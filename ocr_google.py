from google.cloud import vision
import io

def extract_text_google(image_file, api_key):
    client = vision.ImageAnnotatorClient.from_service_account_json(api_key)

    content = image_file.read()
    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description
    else:
        return "No text found"
