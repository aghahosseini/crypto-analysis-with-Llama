
import requests
import json
import time

#API INFORMATION FOR COINMARKETCAP
API_KEY = 'b93b59f9-a416-4a54-8d3b-8bce14229b01' 
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

#api for llama

API_URL = 'https://qwen72b.gaia.domains/v1'


#REQUESTS PARAMETERS
parameters = {
    'start': '1',        # START FOR RANK 1
    'limit': '5',        # Get the top 5 cryptocurrencies
    'convert': 'USD'     # Convert prices to USD
}

# Request headers (including the API key)
headers = {
    'Accept': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY
}


# Fixed file name for storing the latest data
filename = "crypto_prices_latest.json"

#  Continuous update loop
try:
    while True:
        # Send a request to the API
        response = requests.get(url, headers=headers, params=parameters)

        if response.status_code == 200:
            # Convert to Json
            data = response.json()

            # Save into the file
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            print(f"All data are update: {filename}")

        else:
            print(f"Error : {response.status_code}")
            print(response.text)

        # time for update
        time.sleep(60)

except KeyboardInterrupt:
    print("project was stop")




def read_crypto_data(file_name="crypto_prices.json"):
    """
    Reads the latest cryptocurrency prices from a JSON file.
    """
    try:
        with open(file_name, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise Exception("JSON file not found. Make sure to run the price fetcher first.")
    except json.JSONDecodeError:
        raise Exception("Error decoding the JSON file.")



def generate_text_with_llama(prompt):
    api_url = "https://llama8b.gaia.domains/v1/chat/completions"

    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer your_api_key_here"
              }  
    
    data = {
        "model": "llama",
        "messages": [
            {"role": "system", "content": "You are a financial analyst assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(api_url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
    
def main():
     json_file = 'crypto_prices.json' 
     output_file = 'crypto_analysis.json'


     while True:
        try:
            # مرحله 1: دریافت داده‌های ارز دیجیتال
            crypto_data = read_crypto_data()

            if not crypto_data:
                print("No crypto data available. Retrying in 60 seconds...")
                time.sleep(180)
                continue

            # مرحله 2: تولید تحلیل برای هر ارز
            analyses = {}
            for item in crypto_data['data']:
                crypto_name = item['name']
                price = item['quote']['USD']['price']

                prompt = f"The current price of {crypto_name} is ${price:.2f}. Write an analysis or prediction based on this data and Respond with a sentence that includes the word 'KIAN'. Ensure the word appears exactly as spelled."
                print(f"Generating analysis for {crypto_name}...")  # چاپ پیام برای هر ارز

                analysis = generate_text_with_llama(prompt)

                if analysis:
                    analyses[crypto_name] = {"price": price, "analysis": analysis}
                    print(f"Analysis for {crypto_name}:\n{analysis}\n")  # چاپ تحلیل در ترمینال
                else:
                    print(f"Failed to generate analysis for {crypto_name}.")  # اگر تحلیل تولید نشد

            # مرحله 3: ذخیره تحلیل‌ها در فایل خروجی
            with open(output_file, 'w') as file:
                json.dump(analyses, file, indent=4)

            print(f"All analyses saved to {output_file}. Waiting 60 seconds for the next update...")
            time.sleep(60)

        except KeyboardInterrupt:
            print("Program terminated by user.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    

if __name__ == "__main__":
    main()    





