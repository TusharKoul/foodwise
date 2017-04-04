//
//  ViewController.swift
//  foodwise-ios
//
//  Created by Tushar Koul on 4/1/17.
//  Copyright © 2017 Tushar Koul. All rights reserved.
//

import UIKit

import SwiftSpinner


class ViewController: UIViewController, FBSDKLoginButtonDelegate {
    
    let loginButton:FBSDKLoginButton = {
        let button = FBSDKLoginButton()
        button.readPermissions = ["email"]
        return button
    }()

    override func viewDidLoad() {
        super.viewDidLoad()
        
        if FBSDKAccessToken.current() != nil {
            login()
        }
        else {
            addFBLoginButton()
        }
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        SwiftSpinner.hide()
    }
    
    func addFBLoginButton() {
        self.view.addSubview(loginButton)
        loginButton.center = self.view.center
        loginButton.delegate = self
    }

    
    public func loginButton(_ loginButton: FBSDKLoginButton!,
                            didCompleteWith result: FBSDKLoginManagerLoginResult!,
                            error: Error!) {
        login()
    }

    public func loginButtonDidLogOut(_ loginButton: FBSDKLoginButton!) {
        print("logged out")
    }
    
    
    func login() {
        SwiftSpinner.show("Connecting...")
        FacebookHelper.sharedInstance.fetchProfile { (result, error) in
            if error == nil {
                self.showNext()
            }
        }
    }
    
    func showNext() {
        let secondVC = self.storyboard?.instantiateViewController(withIdentifier: "SecondViewController") as! SecondViewController
        self.navigationController?.pushViewController(secondVC, animated: true)
    }
}

