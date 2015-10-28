//
//  WordingService.swift
//  wording
//
//  Created by Cor Pruijs on 27-10-15.
//  Copyright © 2015 Cor Pruijs. All rights reserved.
//

import Foundation

class WordingService {
    var settings: Settings!
    var token: String?
    
    init() {
        self.settings = Settings()
        getToken() { token in
            self.token = token
            print("Token: \(self.token)");
        }
    }
    
    func getToken(onCompletion: (token: String?) -> ()) {
        
        
        // TODO: Make this safe
        let request = NSMutableURLRequest(URL: NSURL(string: "\(settings.ip)authenticate")!)
        print("\(settings.ip)authenticate")
        let session = NSURLSession.sharedSession()
        request.HTTPMethod = "POST"
        let params = ["username": "cor", "password": "Hunter2"]
        
        do {
            request.HTTPBody = try NSJSONSerialization.dataWithJSONObject(params, options: [])
        } catch {
            print(error)
        }
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        request.addValue("application/json", forHTTPHeaderField: "Accept")
        
        
        
        let task = session.dataTaskWithRequest(request) {
            data, response, error in
            
            let token = NSString(data: data!, encoding: NSUTF8StringEncoding)
            onCompletion(token: token as String?)
        }
        
        task.resume()
        
    }
    
    func getLists(callback: (NSDictionary) -> ()) {
        request(settings.ip, callback: callback)
    }
    
    func request(url: String, callback:(NSDictionary) -> ()) {
        
        // the url
        let nsURL = NSURL(string: url)!
        let request = NSMutableURLRequest(URL: nsURL)
        
        // the NSURLSession
        let task = NSURLSession.sharedSession().dataTaskWithURL(nsURL) {
            (data, response, error) in
            
            do {
                if let jsonResult = try NSJSONSerialization.JSONObjectWithData(data!, options: NSJSONReadingOptions.MutableContainers) as? NSDictionary {
                    print(jsonResult)
                    callback(jsonResult)
                }
            } catch {
                print(error)
            }
        }
        task.resume()
    }
}

