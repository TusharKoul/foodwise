//
//  FBPostViewController
//  foodwise-ios
//
//  Created by Tushar Koul on 4/1/17.
//  Copyright © 2017 Tushar Koul. All rights reserved.
//

import Foundation
import SwiftSpinner
import Alamofire
import ImagePicker

class FBPostViewController: UIViewController,ImagePickerDelegate,FBSDKSharingDelegate {
    
    @IBOutlet weak var uploadButton: UIButton!
    
    override func viewDidLoad() {
//        let sessionManager = Alamofire.SessionManager(configuration: URLSessionConfiguration.default)
//        let delegate: Alamofire.SessionDelegate = sessionManager.delegate
//        
//        delegate.taskWillPerformHTTPRedirection = { session, task, response, request in
//            return nil
//        }
        
        let delegate = Alamofire.Manager.sharedInstance.delegate
        delegate.taskWillPerformHTTPRedirection = { session, task, response, request in
            return NSURLRequest(URL: NSURL(string: URL)!)
        }

    }
    
    
    @IBAction func uploadButtonPressed(_ sender: UIButton) {
//        getPhotos()
        processPost()
    }
    
    func getPhotos() {
        var configuration = Configuration()
        configuration.doneButtonTitle = "Finish"
        configuration.noImagesTitle = "Sorry! There are no images here!"
        configuration.recordLocation = false
        
        let imagePickerController = ImagePickerController(configuration: configuration)
        imagePickerController.delegate = self
        present(imagePickerController, animated: true, completion: nil)
    }
    
//
//
//
    func wrapperDidPress(_ imagePicker: ImagePickerController, images: [UIImage]) {
        dismiss(animated: true, completion: nil)
    }
    
    func doneButtonDidPress(_ imagePicker: ImagePickerController, images: [UIImage]) {
        dismiss(animated: true) { 
            self.processImages(images: images)
        }
    }
    
    func cancelButtonDidPress(_ imagePicker: ImagePickerController) {
        dismiss(animated: true, completion: nil)
    }
//    
//    
//    
    
    func processImages(images: [UIImage]) {
        uploadToServer(images: images) { (error) in
            if error == nil {
                self.uploadToFb(images: images)
            }
        }
    }
    
    func uploadToServer(images: [UIImage], completion: @escaping (Error?) -> Void ) {
        AlamoHelper.sharedInstance.uploadImages(images: images) { (error) in
            completion(nil)
        }
    }
    
    func uploadToFb(images: [UIImage]) {
        let fbContent = FacebookHelper.sharedInstance.getFBMediaObject(images: images)
        let fbDialog = FBSDKShareDialog()
        fbDialog.fromViewController = self
        fbDialog.shareContent = fbContent
        fbDialog.delegate = self
        
        fbDialog.mode = .native;
        fbDialog.show()
    }
    
    
    public func sharer(_ sharer: FBSDKSharing!, didCompleteWithResults results: [AnyHashable : Any]!) {
        print(results)
        print("printing results")
        
        processPost()
    }
    
    public func sharer(_ sharer: FBSDKSharing!, didFailWithError error: Error!) {
        print(error)
    }
    
    public func sharerDidCancel(_ sharer: FBSDKSharing!) {
        print(sharer)
    }
    
    
    func processPost() {
        SwiftSpinner.show("Loading...")
        FacebookHelper.sharedInstance.fetchLastPostedStoryId { (resultId, error) in
            guard
                let resultId = resultId as? String
            else {
                return
            }
            
            FacebookHelper.sharedInstance.fetchPost(postId: resultId, completion: { (result, error) in
                SwiftSpinner.hide()
                guard
                    let result = result as? NSDictionary,
                    let creationTime = result["created_time"] as? String,
                    let withTags = result["with_tags"] as? NSDictionary,
                    let taggedFriends = withTags["data"] as? NSArray,
                    let place = result["place"] as? NSDictionary,
                    let placeName = place["name"] as? String,
                    let placeLocation = place["location"] as? NSDictionary,
                    let placeId = place["id"] as? String
                    else {
                        return
                }
                
                let friends = self.populateTaggedFriends(taggedFriends: taggedFriends)
                let placeDetails = PlaceDetails(id: placeId, name: placeName, location: placeLocation)
                
                AlamoHelper.sharedInstance.postFbMetadata(completion: { _ in (error)
                    
                })
            })
        }
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
