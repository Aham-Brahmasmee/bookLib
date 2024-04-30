import os
import pickle
import pandas as pd
from flask import Flask, render_template, request
from scipy.sparse import hstack
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

# Load the books data
books = pd.read_csv(r'C:\USB\BOOKS.csv')

# Initialize the user-item matrix
pt = pd.DataFrame(index=books.index)

# Combine the category and author TF-IDF matrices
file_path = "C:/USB/falcon/tfidf_matrix_categories.pkl"
os.chdir(os.path.dirname(file_path))
with open(file_path, "rb") as f:
    tfidf_matrix_categories = pickle.load(f)

with open('tfidf_matrix_authors.pkl', 'rb') as f:
    tfidf_matrix_authors = pickle.load(f)

tfidf_matrix_combined = hstack((tfidf_matrix_categories, tfidf_matrix_authors))

# Load the pre-trained KNN model
with open('knn_model.pkl', 'rb') as f:
    knn_model = pickle.load(f)

app = Flask(__name__, template_folder='C:/USB/falcon/templates')


def get_book_info(book_title):
    book_info = books[books['Title'] == book_title].iloc[0]
    return {
        'Title': book_info['Title'],
        'Categories': book_info['categories'],
        'Description': book_info['description'],
        'Image_URL': book_info['image'],
        'Author': book_info['authors']
    }
@app.route('/')
def index():
    return render_template('recommender.html')

@app.route('/book_details')
def book_details():
    book_title = request.args.get('book_title')
    book_info = get_book_info(book_title)
    return render_template('recommenderbook_details.html', book_details=book_info)



@app.route('/recommendations', methods=['POST'])

def recommendations():
    global pt
    # Initialize the user-item matrix if it is None
    if pt is None:
        pt = pd.DataFrame(index=books.index)

    # Get the user's favorite book
    book_title = request.form['book_title']

    try:
        # Get the index of the book
        book_idx = books[books['Title'] == book_title].index[0]

        # Get content-based recommendations
        content_similarities = cosine_similarity(tfidf_matrix_combined[book_idx], tfidf_matrix_combined).flatten()
        content_related_books_indices = content_similarities.argsort()[:-11:-1]
        content_recommendations = [get_book_info(books.iloc[idx]['Title']) for idx in content_related_books_indices]

        # Get collaborative-filtering recommendations
        if not pt.empty:
            knn_distances, knn_indices = knn_model.kneighbors(pt.loc[[book_title]], n_neighbors=11)
            collaborative_recommendations = [get_book_info(pt.index[idx]) for idx in knn_indices[0][1:]]
        else:
            collaborative_recommendations = []

        # Combine the recommendations
        hybrid_recommendations = content_recommendations + collaborative_recommendations

        # Render the index.html template with the recommendations
        return render_template('recommender.html', recommendations=hybrid_recommendations[:7])

    except IndexError:
        # Handle the case where the book title is not found
        return render_template('recommender.html', error="Book not found")



if __name__ == '__main__':
    app.run(debug=True)
