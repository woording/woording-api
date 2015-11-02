//
//  Translation.swift
//  wording
//
//  Created by Cor Pruijs on 27-10-15.
//  Copyright © 2015 Cor Pruijs. All rights reserved.
//

import Foundation

typealias IsoCode = String
typealias Translation = [IsoCode: String]

func translationIsCorrect(translation: Translation) -> Bool {
    
    let correctTranslations: [Translation] = [["eng": "car", "dut": "auto"], ["eng": "tree", "dut": "boom"]]
    
    return correctTranslations.contains({$0 == translation})
}