from dotenv import load_dotenv
from openai import OpenAI
import base64

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def call_openai_endpoint(img_path: str):
  system_prompt = """You are an experienced seasoned underwriter working in Senior Living Insurance Facility space. 
  You know all the important information that you need from an application to write the best coverage policy.
  You understand all types of policies like General Liability, Professional Liability, commercial property insurance etc.

  
  """

  

  