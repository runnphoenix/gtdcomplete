//
//  UserViewController.m
//  gtdcomplete
//
//  Created by temp on 2018/2/26.
//  Copyright © 2018年 self. All rights reserved.
//

#import "UserViewController.h"

@interface UserViewController ()
@property (weak, nonatomic) IBOutlet UILabel *nameLabel;
@property (weak, nonatomic) IBOutlet UIButton *logButton;
@property (weak, nonatomic) IBOutlet UIButton *signButton;
@property (weak, nonatomic) IBOutlet UIButton *logOutButton;
@end

@implementation UserViewController

- (void)viewDidLoad {
    [super viewDidLoad];
}

- (void)viewWillAppear:(BOOL)animated {
    NSString *uid = [[NSUserDefaults standardUserDefaults] objectForKey:@"uid"];
    NSString *uname = [[NSUserDefaults standardUserDefaults] objectForKey:@"uname"];
    
    if (uid == nil){
        self.nameLabel.hidden = YES;
        self.logOutButton.hidden = YES;
        self.logButton.hidden = NO;
        self.signButton.hidden = NO;
    }else{
        self.nameLabel.hidden = NO;
        self.nameLabel.text = [NSString stringWithFormat:@"User Name: %@", uname];
        self.logOutButton.hidden = NO;
        self.logButton.hidden = YES;
        self.signButton.hidden = YES;
    }
}

- (IBAction)toLogin {
    //push controller stack
}

- (IBAction)toSignup {
    //push controler stack
}

- (IBAction)logout {
    [[NSUserDefaults standardUserDefaults] setObject:nil forKey:@"uid"];
    [[NSUserDefaults standardUserDefaults] setObject:nil forKey:@"uname"];
    [self viewWillAppear:YES];
}


- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

/*
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}
*/

@end
