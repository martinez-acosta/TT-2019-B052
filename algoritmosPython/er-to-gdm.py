import json 

def main():
  
    # Opening JSON file 
    input_file = open('er.json',) 
    data = json.load(input_file) 
    
    for i in data['emp_details']: 
        print(i) 
    
    # Closing file 
    input_file.close() 
    return

if __name__ == '__main__':
    main()