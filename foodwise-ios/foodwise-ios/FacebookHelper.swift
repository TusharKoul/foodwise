//
//  FacebookHelper.swift
//  foodwise-ios
//
//  Created by Tushar Koul on 4/1/17.
//  Copyright © 2017 Tushar Koul. All rights reserved.
//

import Foundation

class FacebookHelper {
    public static let sharedInstance = FacebookHelper()
    
    var currentUser:UserDetails? = nil
    
    
    func startFacebookActivity() {
        FBSDKAppEvents.activateApp()
    }
    
    
    func fetchProfile(completion: @escaping (Any?, Error?) -> Void) {
        let params = ["fields" : "email, name,id, picture.type(large)"]
        FBSDKGraphRequest(graphPath: "me", parameters: params).start { (connection, result, error) in
            if let error = error {
                completion(nil,error)
                return
            }
            
            guard
                let result = result as? NSDictionary,
                let email = result["email"] as? String,
                let user_name = result["name"] as? String,
                let user_id = result["id"]  as? String
            else {
                completion(nil,nil)
                return
            }
            
            self.currentUser = UserDetails(id: user_id,name: user_name,email: email)
            
            guard
                let picture = result["picture"] as? NSDictionary,
                let data = picture["data"] as? NSDictionary,
                let url = data["url"] as? String
            else {
                completion(nil,nil)
                return
            }
            print(url)
            
            completion(result,nil)
        }
    }
    
    func fetchPost(postId:String, completion: @escaping (Any?, Error?) -> Void) {
        let params = ["fields": "story, description, caption, message, created_time, place, status_type, with_tags"]
        
        FBSDKGraphRequest(graphPath: postId, parameters: params).start { (connection, result, error) in
            if let error = error {
                completion(nil,error)
                return
            }
            
            completion(result,nil)
        }
    }
    
    func fetchLastPostedStoryId(completion: @escaping (Any?, Error?) -> Void) {
        let params = ["fields": "feed.limit(1)"]
        
        FBSDKGraphRequest(graphPath: "me", parameters: params).start { (connection, result, error) in
            if let error = error {
                completion(nil,error)
                return
            }
            guard
                let result = result as? NSDictionary,
                let feed = result["feed"] as? NSDictionary,
                let data = feed["data"] as? NSArray,
                let dataDict = data[0] as? NSDictionary,
                let id = dataDict["id"] as? String
            else {
                completion(nil,nil)
                return
            }
            completion(id,nil)
        }
    }
    
    func getFBMediaObject(images: [UIImage]) -> FBSDKSharePhotoContent{
        var photos:[FBSDKSharePhoto] = []
        for image in images {
            let fbPhoto = FBSDKSharePhoto()
            fbPhoto.image = image
            fbPhoto.isUserGenerated = true
            photos.append(fbPhoto)
        }
        
        let content = FBSDKSharePhotoContent()
        content.photos = photos
        return content
    }

}
