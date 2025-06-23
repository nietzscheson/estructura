class Textract:
    def __init__(self, client):
        self.client = client

    def text_detection(self, image: bytes):
        response = self.client.detect_document_text(Document={"Bytes": image})

        lines = [
            item["Text"] for item in response["Blocks"] if item["BlockType"] == "LINE"
        ]

        return " ".join(lines)
