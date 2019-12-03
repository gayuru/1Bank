//
//  LoginViewController.swift
//  OneBank
//
//  Created by Sogyal Thundup Sherpa on 30/11/19.
//  Copyright © 2019 iSwift. All rights reserved.
//

import UIKit

class LoginViewController: UIViewController {
 
    @IBOutlet weak var passwordField: UITextField!
    @IBOutlet weak var usernameField: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        overrideUserInterfaceStyle = .light
        
        //Looks for single or multiple taps.
        let tap: UITapGestureRecognizer = UITapGestureRecognizer(target: self, action: Selector(("closeKeyboard")))
        
          //Uncomment the line below if you want the tap not not interfere and cancel other interactions.
//          tap.cancelsTouchesInView = false

          view.addGestureRecognizer(tap)
//        let userTappedOtherThanKeyboard: UITapGestureRecognizer = UITapGestureRecognizer(target: self, action: Selector(("closeKeyboard")))
//        view.addGestureRecognizer(userTappedOtherThanKeyboard)
//        
        // Do any additional setup after loading the view.
    }
    
    @objc func closeKeyboard() {
       view.endEditing(true)
    }

    
   
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
