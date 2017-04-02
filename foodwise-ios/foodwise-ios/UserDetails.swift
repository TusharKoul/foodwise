//
//  UserDetails.swift
//  foodwise-ios
//
//  Created by Tushar Koul on 4/2/17.
//  Copyright © 2017 Tushar Koul. All rights reserved.
//

import Foundation

class UserDetails {
    var id:String
    var name:String
    var email:String?
    
    init(id:String, name:String, email:String?) {
        self.name = name
        self.id = id
        self.email = email
    }
    
    public func firstName() -> String {
        let s = self.name.components(separatedBy: " ")
        return s[0]
    }
}
