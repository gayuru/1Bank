//
//  LoginViewController.swift
//  OneBank
//
//  Created by Sogyal Thundup Sherpa on 30/11/19.
//  Copyright © 2019 iSwift. All rights reserved.
//

import UIKit

class LoginViewController: UIViewController {
 
    private let model = RestRequest.shared
    
    override func viewDidLoad() {
        super.viewDidLoad()
        overrideUserInterfaceStyle = .light
        let userTappedOtherThanKeyboard: UITapGestureRecognizer = UITapGestureRecognizer(target: self, action: Selector(("closeKeyboard")))
        view.addGestureRecognizer(userTappedOtherThanKeyboard)
        
        // Do any additional setup after loading the view.
    }
    
    @objc func closeKeyboard() {
           view.endEditing(true)
    }

    
    @IBOutlet weak var passwordField: UITextField!
    @IBOutlet weak var usernameField: UITextField!
    
    @IBAction func loginAction(_ sender: Any) {
        Globals.username = usernameField.text!
    }
    
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
