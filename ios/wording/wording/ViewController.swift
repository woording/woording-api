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
        
        print(translation1["eng"])
        print(translation1["eng"]!)
        print(translation1["bulg"])
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

