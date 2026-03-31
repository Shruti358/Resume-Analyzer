import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer


# Load data
def load_data(file="processed_data.json"):
    with open(file, "r") as f:
        return json.load(f)


# Convert skills to vectors
def vectorize(data):
    mlb = MultiLabelBinarizer()

    all_skills = [item["resume_skills"] + item["job_skills"] for item in data]
    mlb.fit(all_skills)

    resume_vectors = mlb.transform([item["resume_skills"] for item in data])
    job_vectors = mlb.transform([item["job_skills"] for item in data])

    return resume_vectors, job_vectors


# Calculate similarity
def calculate_similarity(resume_vecs, job_vecs):
    scores = []

    for r, j in zip(resume_vecs, job_vecs):
        score = cosine_similarity([r], [j])[0][0]
        scores.append(round(score * 100, 2))  # percentage

    return scores


# Main function
def main():
    data = load_data()

    resume_vecs, job_vecs = vectorize(data)
    scores = calculate_similarity(resume_vecs, job_vecs)

    print("\n📊 MATCHING RESULTS:\n")

    for i, score in enumerate(scores[:10]):  # show first 10
        print(f"Resume {i+1} → Match Score: {score}%")


if __name__ == "__main__":
    main()