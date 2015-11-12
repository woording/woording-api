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
    
    func getToken(onCompletion: (token: String) -> ()) {
        
        if token == nil {
            
            let url = "\(settings.ip)authenticate"
            print("URL: \(url)")
            
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
                onCompletion(token: self.token!)
            }
            
            task.resume()
            
        } else {
            onCompletion(token: self.token!)
        }
        
    }
    
    
    func getLists(callback: (json: JSON) -> ()) {
        request("\(settings.ip)cor") { json in
            print(json)
        }
    }
    
    func request(url: String, callback:(JSON) -> ()) {
        
        getToken {
            
            token in
            print("TOKEN IN REQUEST: \(token)")
            
            let nsURL = NSURL(string: url)!
            let request = NSMutableURLRequest(URL: nsURL)
            let params = ["token" : token]
            
            request.HTTPMethod = "POST"
            do {
                request.HTTPBody = try JSON(params).rawData()
                print("request HTTPBody \(request.HTTPBody)")
            } catch {
                print(error)
            }
            
            
            request.addValue("application/json charset=utf-8", forHTTPHeaderField: "Content-Type")
            request.addValue("application/json", forHTTPHeaderField: "Accept")
            
            
            let session = NSURLSession.sharedSession()
            
            // the NSURLSession
            let task = session.dataTaskWithRequest(request) {
                (data, response, error) in
                
                print("DATA: \(data)")
                print("RESPONSE: \(response)")
                print("ERROR: \(error)")
                
                let jsonResult = JSON(data: data!)
                
                callback(jsonResult)
            }
            
            task.resume()
        }
    }
}

