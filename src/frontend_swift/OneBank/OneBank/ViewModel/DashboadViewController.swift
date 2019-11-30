//
//  DashboadViewController.swift
//  OneBank
//
//  Created by Sogyal Thundup Sherpa on 30/11/19.
//  Copyright © 2019 iSwift. All rights reserved.
//

import UIKit

class DashboadViewController: UIViewController {

    @IBOutlet weak var setttingsView: UIView!
    @IBOutlet weak var usernameLabel: UILabel!
    @IBOutlet weak var profileImage: UIImageView!
    override func viewDidLoad() {
        super.viewDidLoad()
        setup()
        // Do any additional setup after loading the view.
    }
    
    func setup(){
        setttingsView.layer.cornerRadius = 5
        profileImage.layer.cornerRadius = profileImage.frame.size.width / 2
        profileImage.clipsToBounds = true
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
