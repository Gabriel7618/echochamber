import os

from groq import Groq

def classify(topic, title, body, maxlen=2000):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"),)

    prompt = (
        "Classify this article as being supportive, opposing or neutral about "
        f"{topic}.\n"
        "Respond with exactly \"1\" if supportive, \"-1\" if opposing or "
        "\"0\" if neutral.\n\n"
        f"Title = \"{title}\"\n\n"
        f"Body = \"{body[:maxlen]}\""
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    classification = chat_completion.choices[0].message.content

    if "-" in classification:
        return -1
    elif "0" in classification:
        return 0
    else:
        return 1


if __name__ == "__main__":
    import pandas as pd
    import numpy as np

    from sklearn.metrics import confusion_matrix


    labels = [0, 1, -1]

    article_n = 15
    is_equal = True

    test_df = pd.read_csv(
        "classifier-data/trump_articles.csv",
        usecols=["title", "text", "topic", "label"],
    )


    def map_classification(label):
        match label:
            case "supportive":
                return 1
            case "opposing":
                return -1
            case "neutral":
                return 0
            case _:
                raise ValueError("Dataset contains invalid label")

    test_df["label"] = test_df["label"].map(map_classification)

    if is_equal:
        pos_test_df = test_df.loc[test_df["label"] == 1]
        pos_test_df = pos_test_df.sample(n=article_n // 3)
        neg_test_df = test_df.loc[test_df["label"] == -1]
        neg_test_df = neg_test_df.sample(n=article_n // 3)
        neu_test_df = test_df.loc[test_df["label"] == 0]
        neu_test_df = neu_test_df.sample(n=article_n // 3)

        test_df = pd.concat([pos_test_df, neg_test_df, neu_test_df])

    else:
        test_df = test_df.sample(n=article_n)

    pred_labels = test_df.apply(
        lambda row: classify(row["topic"], row["title"], row["text"]),
        axis=1
    )

    accuracy = pred_labels.loc[
        pred_labels == test_df["label"]
    ].size / article_n

    cm = confusion_matrix(test_df["label"], pred_labels, labels=labels)

    print(f"Accuracy: {accuracy}\n")
    print("Confusion Matrix:")
    print(pd.DataFrame(cm, index=labels, columns=labels), end="\n\n")

