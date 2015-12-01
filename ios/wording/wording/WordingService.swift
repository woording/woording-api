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
    let connection: WordingConnection
    
    init() {
        connection = WordingConnection()
    }
    
    func getUser(user: String, callback: (JSON) -> ()) {
        connection.request(connection.settings.ip + user) {
            json in
            callback(json)
        }
    }
    
    func getList(user: String, listname: String, callback: (JSON) -> ()) {
        connection.request(connection.settings.ip + user + "/" + listname) {
            json in
            callback(json)
        }
    }
    
    
}

