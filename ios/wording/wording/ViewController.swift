//
//  ViewController.swift
//  wording
//
//  Created by Cor Pruijs on 22-09-15.
//  Copyright © 2015 Cor Pruijs. All rights reserved.
//

import UIKit

class ViewController: UIViewController {
    
    

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        let translation1: Translation = ["eng": "car", "dut": "auto"]
        let translation2: Translation = ["eng": "cer", "dut": "auto"]
        
        print(translation1["eng"])
        print(translation1["eng"]!)
        print(translation1["bulg"])
        
        print(translationIsCorrect(translation1))
        print(translationIsCorrect(translation2))
        
        let wordingService = WordingService()
        
        wordingService.getUser("cor") {
            json in
            print(json)
        }
        
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

