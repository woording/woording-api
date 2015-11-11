//
//  WordingService.swift
//  wording
//
//  Created by Cor Pruijs on 27-10-15.
//  Copyright © 2015 Cor Pruijs. All rights reserved.
//

import Foundation
import SwiftyJSON

class WordingService {
    var settings: Settings!
    var token: String?
    
    init() {
        self.settings = Settings()
    }
    
    func getToken(onCompletion: (token: String?) -> ()) {
        
        if token == nil {
            
            let url = "\(settings.ip)authenticate"
            print("URL: \(settings.ip)authenticate")
            
            let request = NSMutableURLRequest(URL: NSURL(string: url)!)
            request.HTTPMethod = "POST"
            
            let session = NSURLSession.sharedSession()
            let params = ["username": "cor", "password": "Hunter2"]
            
            do {
                request.HTTPBody = try JSON(params).rawData()
            } catch {
                print(error)
            }
            
            request.addValue("application/json charset=utf-8", forHTTPHeaderField: "Content-Type")
            request.addValue("application/json", forHTTPHeaderField: "Accept")
            
            
            let task = session.dataTaskWithRequest(request) {
                data, response, error in
                
                print("DATA: \(data)")
                print("RESPONSE: \(response)")
                print("ERROR: \(error)")
                
                let json = JSON(data: data!)
                self.token = json["token"].stringValue
                onCompletion(token: self.token)
            }
            
            task.resume()
            
        } else {
            
            onCompletion(token: token)
        }
        
        
    }
    
    
    func getLists(callback: (NSDictionary) -> ()) {
        request(settings.ip, callback: callback)
    }
    
    func request(url: String, callback:(NSDictionary) -> ()) {
        
        // the url
        let nsURL = NSURL(string: url)!
        let request = NSMutableURLRequest(URL: nsURL)
        
//        let params = ["token": ]
        
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

