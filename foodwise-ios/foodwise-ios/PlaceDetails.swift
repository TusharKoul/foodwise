//
//  PlaceDetails.swift
//  foodwise-ios
//
//  Created by Tushar Koul on 4/2/17.
//  Copyright © 2017 Tushar Koul. All rights reserved.
//

import Foundation

class PlaceDetails {
    var id:String
    var name:String
    var location:NSDictionary?
    
    init(id:String, name:String, location:NSDictionary?) {
        self.name = name
        self.id = id
        self.location = location
    }
}
