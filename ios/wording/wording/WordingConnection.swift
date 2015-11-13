//
//  WordingConnection.swift
//  wording
//
//  Created by Cor Pruijs on 12-11-15.
//  Copyright © 2015 Cor Pruijs. All rights reserved.
//

import Foundation
import SwiftyJSON

class WordingConnection {
    
    var settings: Settings!
    var token: String?
    
    init() {
        self.settings = Settings()
    }
    
    func getToken(onCompletion: (token: String) -> ()) {
        
        if token != nil {
            // use a cached token if it is available
            onCompletion(token: self.token!)
        
        } else {
            
            // there is no cached token available, so we'll request a new one
            
            let url = "\(settings.ip)authenticate"
            
            // Create a new request
            let request = NSMutableURLRequest(URL: NSURL(string: url)!)
            
            // Set up the HTTP Method
            request.HTTPMethod = "POST"
            
            // Set the HTTP Header Fields
            request.addValue("application/json charset=utf-8", forHTTPHeaderField: "Content-Type")
            request.addValue("application/json", forHTTPHeaderField: "Accept")
            
            // Set up the HTTP Body and fill it with the required data
            let params = ["username": "cor", "password": "Hunter2"]
            do {
                request.HTTPBody = try JSON(params).rawData()
            } catch {
                print(error)
            }
            
            // Create a NSUrlSessionDataTask
            let session = NSURLSession.sharedSession()
            let task = session.dataTaskWithRequest(request) {
                
                data, response, error in
                
                // if there's an error, print it and also print the data and response
                if error != nil {
                    print("DATA: \(data)")
                    print("RESPONSE: \(response)")
                    print("ERROR: \(error)")
                }
                
                // Create a JSON object from the retrieved data
                let json = JSON(data: data!)
                
                // Retrieve the token from the json object and cache it
                self.token = json["token"].stringValue
                
                // Send the now cached token to the onCompletion block
                onCompletion(token: self.token!)
            }
            
            task.resume()
            
        }
    }
    
    
    func request(url: String, callback:(JSON) -> ()) {
        
        getToken {
            
            token in
            
            let url = NSURL(string: url)
            
            // Create a new request
            let request = NSMutableURLRequest(URL: url!)
            
            // Set up the HTTP Method
            request.HTTPMethod = "POST"
            
            // Set the HTTP Header Fields
            request.addValue("application/json charset=utf-8", forHTTPHeaderField: "Content-Type")
            request.addValue("application/json", forHTTPHeaderField: "Accept")
            
            // Set up the HTTP Body and fill it with the required data
            let params = ["token" : token]
            do {
                request.HTTPBody = try JSON(params).rawData()
            } catch {
                print(error)
            }
            
            // Create a NSUrlSessionDataTask
            let session = NSURLSession.sharedSession()
            let task = session.dataTaskWithRequest(request) {
                
                data, response, error in
                
                // if there's an error, print it and also print the data and response
                if error != nil {
                    print("DATA: \(data)")
                    print("RESPONSE: \(response)")
                    print("ERROR: \(error)")
                }
                
                // Create a JSON object from the retrieved data
                let json = JSON(data: data!)
                
                // Pass the JSON data to the callback
                callback(json)
            }
            
            task.resume()
        }
    }
}
