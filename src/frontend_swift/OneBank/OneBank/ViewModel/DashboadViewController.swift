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
    @IBOutlet weak var cardCollectionView: UICollectionView!
    @IBOutlet weak var servicesCollectionView: UICollectionView!
    @IBOutlet weak var transactionsTableView: UITableView!
    override func viewDidLoad() {
        super.viewDidLoad()
        setup()
        cardCollectionView.delegate = self
        cardCollectionView.dataSource = self
        servicesCollectionView.delegate = self
        servicesCollectionView.dataSource = self
        transactionsTableView.delegate = self
        transactionsTableView.dataSource = self
        // Do any additional setup after loading the view.
    }
    
    func setup(){
        setttingsView.layer.cornerRadius = 5
        profileImage.layer.cornerRadius = profileImage.frame.size.width / 2
        profileImage.clipsToBounds = true
    }
}

extension DashboadViewController: UICollectionViewDelegate,UICollectionViewDataSource{

    
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        if collectionView == cardCollectionView{
            return 5
        }else{
            return 8
        }
        
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        if collectionView == cardCollectionView{
            let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "cardCell", for: indexPath) as! CardCollectionViewCell
            cell.balanceLabel.textColor = .black
            cell.balanceLabel.text = "$100.00"
            if indexPath.row  == 0{
                let radius: CGFloat = 10
                cell.layer.cornerRadius = radius
                cell.layer.shadowColor = UIColor.init(red: 189, green: 208, blue: 240).cgColor
                cell.layer.shadowOffset = CGSize(width: 0, height: 1.0)
                cell.layer.shadowRadius = 3.0
                cell.layer.shadowOpacity = 0.5
                // Never mask the shadow as it falls outside the view
                cell.layer.masksToBounds = false
                cell.cardTypeImage.image = UIImage(named: "")
                cell.bankImage.image = UIImage(named: "")
                cell.balanceLabel.numberOfLines = 1
                cell.frame.origin.y = 50
            }
            
            return cell
        }else{
            let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "servicesCell", for: indexPath) as! ServicesCollectionViewCell
//            cell.backgroundView?.backgroundColor = UIColor(red: 224, green: 236, blue: 255)
//            cell.backgroundView.backgroundColor = UIColor(red: 224, green: 236, blue: 255)
            return cell
        }
    }
}


extension DashboadViewController: UITableViewDelegate,UITableViewDataSource{
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 4
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "transactionCell", for: indexPath) as! TransactionsTableViewCell
        
        cell.companyNameLabel.text = "Spotify"
        cell.amountSpendLabel.text = "$200.0"
        cell.timeAgoLabel.text = "5 hours ago"
        cell.categoryView.layer.cornerRadius = cell.categoryView.frame.size.width / 2
        return cell
    }
    
    
}

//MARK:- UIColor Extensions for HexCode
extension UIColor {
    convenience init(red: Int, green: Int, blue: Int) {
        assert(red >= 0 && red <= 255, "Invalid red component")
        assert(green >= 0 && green <= 255, "Invalid green component")
        assert(blue >= 0 && blue <= 255, "Invalid blue component")
        
        self.init(red: CGFloat(red) / 255.0, green: CGFloat(green) / 255.0, blue: CGFloat(blue) / 255.0, alpha: 1.0)
    }
    
    convenience init(rgb: Int) {
        self.init(
            red: (rgb >> 16) & 0xFF,
            green: (rgb >> 8) & 0xFF,
            blue: rgb & 0xFF
        )
    }
}
