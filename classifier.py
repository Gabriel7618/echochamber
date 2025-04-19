import os

from groq import Groq


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def classify(topic, title, body):
    """
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": (
                        "Say Hello World!"
                    ),
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    print(chat_completion.choices[0].message.content)
    """

    return 0


if __name__ == "__main__":
    import pandas as pd
    import numpy as np

    from sklearn.metrics import confusion_matrix


    labels = [0, 1, -1]

    topic = "Trump"

    article_n = 30
    is_equal = True
    is_politics_only = True
    title_contains = None
    body_contains = "trump"

    test_df = pd.read_csv(
        "classifier-data/trump_articles.csv",
        usecols=["title", "text", "subject", "label"],
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

    if is_politics_only:
        test_df = test_df.loc[test_df["subject"] == "politicsNews"]

    if title_contains:
        test_df = test_df.loc[
            test_df["title"].str.contains(title_contains, case=False)
        ]

    if body_contains:
        test_df = test_df.loc[
            test_df["text"].str.contains(body_contains, case=False)
        ]

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
        lambda row: classify(topic, row["title"], row["text"]),
        axis=1
    )

    accuracy = pred_labels.loc[
        pred_labels == test_df["label"]
    ].size / article_n

    cm = confusion_matrix(test_df["label"], pred_labels, labels=labels)

    print(f"Accuracy: {accuracy}\n")
    print("Confusion Matrix:")
    print(pd.DataFrame(cm, index=labels, columns=labels))

