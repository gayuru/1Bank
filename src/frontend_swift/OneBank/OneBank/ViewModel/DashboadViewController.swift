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
        overrideUserInterfaceStyle = .light
        transactionsTableView.allowsSelection = false
        setup()
        cardCollectionView.delegate = self
        cardCollectionView.dataSource = self
        servicesCollectionView.delegate = self
        servicesCollectionView.dataSource = self
        transactionsTableView.delegate = self
        transactionsTableView.dataSource = self
        cardCollectionView.backgroundColor = UIColor.clear
        servicesCollectionView.backgroundColor = UIColor.clear
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
            return 4
        }
        
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        if collectionView == cardCollectionView{
            let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "cardCell", for: indexPath) as! CardCollectionViewCell
            cell.balanceLabel.textColor = .black
            
            let radius: CGFloat = 10
            cell.layer.cornerRadius = radius
            switch indexPath.row {
            case 0:
                cell.layer.shadowColor = UIColor.init(red: 189, green: 208, blue: 240).cgColor
                cell.layer.shadowOffset = CGSize(width: 0, height: 1.0)
                cell.layer.shadowRadius = 3.0
                cell.layer.shadowOpacity = 0.5
                // Never mask the shadow as it falls outside the view
                cell.balanceLabel.text = ""
                cell.balanceType.text = ""
                cell.layer.masksToBounds = false
                cell.cardTypeImage.image = UIImage(named: "")
                cell.bankImage.image = UIImage(named: "")
                cell.balanceLabel.numberOfLines = 1
                cell.frame.origin.y = 40
                break;
            case 1:
                cell.totalBalance.text = ""
               cell.totalBalanceLabel.text = ""
               cell.balanceLabel.text = "$1279.00"
               cell.balanceLabel.textColor = UIColor.white
               cell.logo.image = UIImage(named: "")
               cell.contentView.backgroundColor = UIColor(red:1.00, green:0.80, blue:0.00, alpha:1.0)
                break;
            case 2:
             cell.totalBalance.text = ""
            cell.totalBalanceLabel.text = ""
            cell.balanceLabel.text = "$4579.00"
            cell.balanceLabel.textColor = UIColor.white
            cell.logo.image = UIImage(named: "")
            cell.contentView.backgroundColor = UIColor(red:0.58, green:0.80, blue:1.00, alpha:1.0)
             break;
                
            case 3:
             cell.totalBalance.text = ""
            cell.totalBalanceLabel.text = ""
            cell.balanceLabel.text = "$6000.00"
            cell.balanceLabel.textColor = UIColor.white
            cell.logo.image = UIImage(named: "")
            cell.contentView.backgroundColor = UIColor(red:0.75, green:0.05, blue:0.00, alpha:1.0)
             break;
            case 4:
             cell.totalBalance.text = ""
            cell.totalBalanceLabel.text = ""
            cell.balanceLabel.text = "$721.00"
            cell.balanceLabel.textColor = UIColor.white
            cell.logo.image = UIImage(named: "")
            cell.contentView.backgroundColor = UIColor(red:1.00, green:0.30, blue:0.44, alpha:1.0)
             break;
            default:
                break;
                
            }
        
            
            return cell
        }else{
            let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "servicesCell", for: indexPath) as! ServicesCollectionViewCell
            cell.servicesView.backgroundColor = UIColor(red: 224, green: 236, blue: 255)
            cell.layer.cornerRadius = 10
            
            return cell
        }
    }
    
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        if collectionView == servicesCollectionView{
            performSegue(withIdentifier: "goToAccount", sender: self)
        }
    }
    
}


extension DashboadViewController: UITableViewDelegate,UITableViewDataSource{
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 4
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "transactionCell", for: indexPath) as! TransactionsTableViewCell
        cell.companyLogo.image = UIImage(named: "spotify")
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
