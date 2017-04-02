//
//  SecondViewController.swift
//  foodwise-ios
//
//  Created by Tushar Koul on 4/1/17.
//  Copyright © 2017 Tushar Koul. All rights reserved.
//

import Foundation
import SwiftSpinner
import Alamofire

class SecondViewController: UIViewController,UIImagePickerControllerDelegate,UINavigationControllerDelegate {
    
    @IBOutlet weak var uploadButton: UIButton!
    
    let imagePicker:UIImagePickerController = {
        let imagePicker = UIImagePickerController()
        imagePicker.sourceType = .photoLibrary
        return imagePicker
    }()
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
    @IBAction func uploadButtonPressed(_ sender: UIButton) {
//        loadFbPost()
        getPhoto()
    }
    
    func getPhoto() {
        imagePicker.delegate = self
        present(imagePicker, animated: true, completion: nil)
    }
    
    public func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any]) {
        if let pickedImage = info[UIImagePickerControllerOriginalImage] as? UIImage {
            
            //AlamoHelper.sharedInstance.uploadImage(image: pickedImage, completion: { (error) in
                
            //})
            
            
        }
        
        dismiss(animated: true, completion: nil)
    }
    
    func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
        dismiss(animated : true, completion: nil)
    }
    
    func loadFbPost() {
        SwiftSpinner.show("Loading...")
//        FacebookHelper.sharedInstance.fetchPost { (result, error) in
//            guard
//                let result = result as? NSDictionary,
//                let creationTime = result["created_time"] as? String,
//                let picUrl = result["full_picture"] as? String,
//                let withTags = result["with_tags"] as? NSDictionary,
//                let taggedFriends = withTags["data"] as? NSArray,
//                let place = result["place"] as? NSDictionary,
//                let placeName = place["name"] as? String,
//                let placeLocation = place["location"] as? NSDictionary,
//                let placeId = place["id"] as? String
//            else {
//                return
//            }
//            
//            let friends = self.populateTaggedFriends(taggedFriends: taggedFriends)
//            let placeDetails = PlaceDetails(id: placeId, name: placeName, location: placeLocation)
//            AlamoHelper.sharedInstance.downloadFile(fileUrl: picUrl, completion: { (error) in
//                SwiftSpinner.hide()
//            })
//        }
    }
    
    func populateTaggedFriends(taggedFriends:NSArray) -> Array<UserDetails> {
        var friends : [UserDetails] = Array()
        for f in taggedFriends {
            guard
                let f = f as? NSDictionary,
                let id = f["id"] as? String,
                let name = f["name"] as? String
            else {
                continue
            }
            let friendDetails = UserDetails(id: id, name: name, email: nil)
            friends.append(friendDetails)
        }
        return friends
    }
    
}
