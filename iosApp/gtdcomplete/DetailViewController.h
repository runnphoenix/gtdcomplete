//
//  DetailViewController.h
//  gtdcomplete
//
//  Created by temp on 2018/2/24.
//  Copyright © 2018年 self. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface DetailViewController : UIViewController

@property (strong, nonatomic) NSDate *detailItem;
@property (weak, nonatomic) IBOutlet UILabel *detailDescriptionLabel;

@end

