//
//  AlamoHelper.swift
//  foodwise-ios
//
//  Created by Tushar Koul on 4/2/17.
//  Copyright © 2017 Tushar Koul. All rights reserved.
//

import Foundation
import Alamofire
import SwiftSpinner

class AlamoHelper {
    public static let sharedInstance = AlamoHelper()
    
    func postFbMetadata(completion:@escaping (Error?) -> Void) {
        let parameters: Parameters = [
            "location": "",
            "emails": ["Swathi@a.com", "Mridul@a.com"],
            "people": ["Swathi", "Mridul"],
            "tod": "lunch",
            "restaurantName":"Il Tramezzino"
        ]
        
        Alamofire.request("https://shrouded-temple-42181.herokuapp.com//metadata", method: .post, parameters: parameters).responseJSON { response in
            print(response.request as Any)  // original URL request
            print(response.response as Any) // URL response
            print(response.result.value as Any)   // result of response serialization
            completion(nil)
        }
    }

    func uploadImages(images:[UIImage], completion:@escaping (Error?) -> Void) {
        Alamofire.upload(
            multipartFormData: { multipartFormData in
                for image in images {
                    let imageData = UIImagePNGRepresentation(image)
                    multipartFormData.append(imageData!, withName: "img")
                }
        },
            to: "https://shrouded-temple-42181.herokuapp.com//upload",
            encodingCompletion: { encodingResult in
                switch encodingResult {
                case .success(let upload, _, _):
                    upload.responseJSON { response in
                        debugPrint(response)
                        SwiftSpinner.hide()
                        completion(nil)
                    }
                    upload.uploadProgress(closure: { //Get Progress
                        progress in
                        SwiftSpinner.show(progress: progress.fractionCompleted, title: "Uploading...")
                    })
                case .failure(let encodingError):
                    print(encodingError)
                    completion(encodingError)
                    SwiftSpinner.hide()
                }
        })
    }
}
