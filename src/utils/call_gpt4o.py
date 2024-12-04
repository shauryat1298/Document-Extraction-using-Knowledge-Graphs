from dotenv import load_dotenv
from openai import OpenAI
import base64
import os
from pathlib import Path
import json

example_img_1_path = Path(r"C:\Users\shaur\Desktop\Learnings\KG_Tests\senior_living_dm\artifacts\applications\chunked_pngs\crc_app_1_4.png")
example_img_2_path = Path(r"C:\Users\shaur\Desktop\Learnings\KG_Tests\senior_living_dm\artifacts\applications\chunked_pngs\crc_app_3_4.png")

client = OpenAI()

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def call_openai_endpoint(img_path: str):

  system_prompt = """You are an experienced seasoned underwriter working in Senior Living Insurance Facility space. 
  You know all the important information that you need from an application to write the best coverage policy.
  You understand all types of policies like General Liability, Professional Liability, commercial property insurance etc.

  You will be provided with image chunks of application form. Find information on these entities in the image chunk: 1. Facility, 2. Residents,
  3. Claims history, 4. Licensing and Ceritfication, 5. Authorized representatives, 6. Risk Management, 7. Contracted Services, 
  8. Physical Premises and Security, 9. Corporate Structure, 10. Bed Census and Occupancy, 11. Coverage, 12. Services, 13. Incidents, 14. Staffing.

  Output in JSON format, and do not output any explanation.
  """

  example_prompt_1 = """
  Facility Information

  Facility Name: Senior Living LLC
  Facility Address: 1234 Northside Blvd
  City: Richardson    State: TX    Zip: 75080
  Federal Employer ID #: 12-3424221
  Administrator Name: Ricky Bahal    Telephone: 838-332-2839
  Email Address: ricky@seniorliving.com    Fax: (___)___-____

  How many years has the facility been under: Present ownership? 5   Present management? 3

  Has the facility had its license suspended, revoked, placed on probation in the last 5 years? ☐ Yes ☑ No
    If yes, please explain: ________________________

  Has Medicare or Medicaid certification been suspended or revoked in the last 3 years? ☐ Yes ☑ No
    If yes, please explain: ________________________

  Has a state or federal agency fined this facility in the last 3 years? ☐ Yes ☑ No

  Has the applicant been designated as a Special Focus Facility within the past 2 years? ☐ Yes ☑ No
  """

  assistant_prompt_1 = {
    "Facility":{
      "name": "Senior Living LLC",
      "address": {
        "add_ln_1": "1234 Northside Blvd",
        "add_ln_2": "",
        "city": "Richardson",
        "state": "TX",
        "zip": "75080"
      },
      "fein": "12-3424221",
      "years_under_present_ownership": 5,
      "years_under_present_management": 3,
      "license_revoked_in_5_years": False,
      "medicare_certifacted_suspended_in_3_years": False,
      "fined_in_3_years": False,
    },

    "Staffing":{
      "key_personnel":{
        "role": "Administrator",
        "name": "Ricky Bahal",
        "telephone": "838-332-2839",
        "email": "ricky@seniorliving.com"
      }
    }
  }
  assistant_prompt_1 = json.dumps(assistant_prompt_1)

  example_prompt_2 = """
  Director of Nursing (DON): Name: Julian Caeser ☐ RN ☐ LPN  
  Length of time at this facility: 12   Length of time as DON: 5  
  Total Number of Director of Nursing at the Facility in the last 5 years: 1  
  Total # of nurse employees: 23  

  Category            | 1st shift | 2nd shift | 3rd shift | Turnover %  
  --------------------|-----------|-----------|-----------|------------  
  RN                 |      3    |      2    |           |   100%  
  LPN/LVN            |      2    |      3    |           |    80%  
  CNA/Personal Caregiver | 1    |      4    |           |    80%  
  Agency / Pool      |      4    |      3    |     1     |   87.5%  

  Do you require nurses to carry malpractice coverage? ☐ Yes ☑ No  
  Do you verify nursing licenses & CRNA certification upon hire and annually? ☑ Yes ☐ No  
  Are background checks completed for agency and pool employees? ☑ Yes ☐ No  
  Are any employees members of a labor union? ☐ Yes ☑ No  

  Are Criminal Background Checks and Sexual Offender Registry Searches performed regularly on ALL staff and volunteers? ☑ Yes ☐ No  
    If “No”, please explain: ______________________  

  Total number of volunteers? 4  
  Is there a formal screening & orientation process? ☑ Yes ☐ No  

  Do volunteers assist with resident feeding? ☑ Yes ☐ No  
  """
  assistant_prompt_2 = {
    "Staffing":{
      "key_personnel":{
        "role": "Director of Nursing",
        "name": "Julian Caeser",
        "years_in_facility": 12,
        "years_as_director_of_nursing": 5,
      },
      "staffing_levels":[
        {
          "staff_type": "RN",
          "first_shift": 3,
          "second_shift": 2,
          "third_shift": 0,
          "turnover_percentage": 100
        },
        {
          "staff_type": "LPN/LVN",
          "first_shift": 2,
          "second_shift": 3,
          "third_shift": 0,
          "turnover_percentage": 80
        },{
          "staff_type": "CNA/Personal Caregiver",
          "first_shift": 1,
          "second_shift": 4,
          "third_shift": 0,
          "turnover_percentage": 80
        },{
          "staff_type": "Agency/Pool",
          "first_shift": 4,
          "second_shift": 3,
          "third_shift": 1,
          "turnover_percentage": 87.5
        },
      ],
      "total_number_of_nurses": 23,
      "nurses_require_malpractice_coverage": False,
      "verify_nurses_license": True,
      "background_check": True,
      "employees_member_of_labor_union": True,
      "criminial_background_check": True,
      "number_of_volunteers": 4,
      "volunteer_assist_in_resident_feeding": True
    }
  }
  assistant_prompt_2 = json.dumps(assistant_prompt_2)

  inference_message = encode_image(img_path)

  messages = [
    {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
    {"role": "user","content": [{ "type": "text", "text": example_prompt_1}]},
    {"role": "assistant","content": [{ "type": "text", "text": assistant_prompt_1}]},
    {"role": "user","content": [{ "type": "text", "text": example_prompt_2}]},
    {"role": "assistant","content": [{ "type": "text", "text": assistant_prompt_2 }]},
    {"role": "user","content": [{ "type": "text", "text": inference_message}]},
  ]

  completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
  )
  
  return completion.choices[0].message.content

  


  

  