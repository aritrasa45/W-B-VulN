import requests
import argparse 
import socket
import random
import time
import os
import sys



R = '\033[31m' # red 
G = '\033[32m' # green 
Y = '\033[33m' # yellow
B = '\033[34m' # blue
C = '\033[36m' # cyan
M = '\033[35m' # magenta

E = '\033[0m' # end
BLD = '\033[1m' # bold



parser = argparse.ArgumentParser(description='WEB-VULN V1 How to use ------->>>')

parser.add_argument('url', type=str, help='the url to ping for ex (google.com) ', default=None)

parser.add_argument('--timeout', type=int, help= 'its the script timeout when the script exits after certain amount of get request',  default = 100000 )

parser.add_argument('--sleep', type=int, help= 'the short delay before doing next ping [default: 0]',  default = 0 )


parser.add_argument('--retry', type=int, help= 'to retry again if the script fails to run due to any errors',  default = 0 )

parser.add_argument('--data', type=str, help= ' to send some data to the given url',  default = None )

parser.add_argument('--proxy', type=str, help= ' to send get requests with given proxy',  default = None )

parser.add_argument('--params', type=str, help= ' to send parameters to the given url',  default = None )

parser.add_argument('--method', type=str, help= ' the method to send data [PUT , DELETE , GET , POST ]',  default = "get" )



args = parser.parse_args()


def kill_processes(error):
    
    if args.retry > 0:
        
        args.retry -= 1
        print(error)
        print(f"[{R}{args.retry}{E}] Left {G}TRYING AGAIN -> {E} ")
        time.sleep(args.sleep)

    else:
        time.sleep(args.sleep)
        print(error)
        sys.exit()
        
 


                              
def open_file(filename):
    
    try:
    
        with open(filename , "r") as f:
            content = f.read()
            return content
            print("{filename} : Found")

    except Exception as e:
        kill_processes(e)

def check_connection():
    
    count = 0
    
    print(f"[!] {Y} checking the connection before starting {E}")
    while count != 5:
        
        try:
        
            requests.get("https://" + args.url)
            
            count += 1
            print(f"{BLD}checking the url connection {count}/5 {E}")
            time.sleep(args.sleep)
        
        
        except KeyboardInterrupt:
            print("\nabort\n")
            sys.exit(0)
            
        except requests.RequestException as e:           
            print("[!] {R}Some kind of obstacles is blocking | its advisable to use more --sleep | numers | TRYING AGAIN {E}")
            kill_processes(e)

                


proxies = []
datas = []
parameters = []   
                                                                                                                                                                     
def send_data(url):
    
    
    if len(proxies) > 0:
        
        proxies_db = {
        
            "http": random.choice(proxies) , 
            "https": random.choice(proxies) ,
        
        }
        print("proxy found from {G}{args.proxy}{E} | len : {len(proxies)}")
        time.sleep(args.sleep)
        
    
    else:
        proxies_db = args.proxy
        print(f"Proxies : {R}{args.proxy} {E}")
        time.sleep(args.sleep)
        
    if len(datas) > 0:
        
        data_db = random.choice(datas)
        print(f"Fetched all data From {R}{args.data}{E} | len : {len(datas)}")
        time.sleep(args.sleep)
        
    else:
        data_db = args.data
        print(f"Trying with data : {G}{args.data}{E}")        
        time.sleep(args.sleep)        

                                                                
    if len(parameters) > 0:
        parami_db = random.choice(parameters)
        print(f"parameters found and saved as randomised..len : {len(parameters)}")
        time.sleep(args.sleep)
        
        
    else:
        parami_db = args.params
        print(f"parameters : {Y}{args.params}{E}")

                                                                                                                                          
    print(f"{args}")
    
    while args.timeout != 0:
    
        try:
        
        
            start_time = time.time()  
            response = getattr(requests , args.method.lower())("https://" + url ,  proxies = proxies_db , data = data_db , params = parami_db)
            end_time = time.time()
        
            total = round(end_time - start_time, 2)
                    
            print(f"[{B}{args.method.upper()}{E}] | {M}{args.url}{E} : returned response_code -> {response.status_code} | ms {C}{total}{E} | ")
            args.timeout -= 1
            time.sleep(args.sleep)
            
            
        
        except KeyboardInterrupt:
            print("\nabort\n")
            sys.exit()
            
                  
        except requests.RequestException as req_excp:
            kill_processes(req_excp)   
            time.sleep(args.sleep)
        



methods_db = ["POST", "PUT", "DELETE", "GET"]
def main():
    
    if not args.method.upper() in methods_db:
        print(f"supported argument :->\n {methods_db}")
        sys.exit()
    
    if not args.data is None and  args.data.endswith(".txt"):
        data_content = open_file(args.data)
        datas.append(data_content)
        time.sleep(args.sleep)
        
                                                   

    if  not args.proxy is None and args.proxy.endswith(".txt"):
        proxy_content = open_file(args.proxy)
        proxies.append(proxy_content)
        time.sleep(args.sleep)
        
    elif not args.proxy is None:
        
        try:
            host , port = args.proxy.split(":")
            socket.inet_aton(host)
            print(f"proxy is valid : {G}TRYING ->{E}")
            proxies.append(args.proxy)
            time.sleep(args.sleep)        
        
        except Exception as sock_excp:
            kill_processes(sock_excp)
            args.proxy = None
            print(f"{R}PROXY INVALID{E} | trying without proxy ->")
            time.sleep(args.sleep)        

    if not args.params is None and args.params.endswith(".txt"):
        params_content = open_file(args.params)
        parameters.append(params_content)
        time.sleep(args.sleep)


    check_connection()
    send_data(args.url)


if __name__ == '__main__':
    main()

