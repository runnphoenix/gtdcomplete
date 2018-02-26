//
//  LoginViewController.m
//  gtdcomplete
//
//  Created by temp on 2018/2/26.
//  Copyright © 2018年 self. All rights reserved.
//

#import "LoginViewController.h"

@interface LoginViewController ()
@property (weak, nonatomic) IBOutlet UITextField *nameTF;
@property (weak, nonatomic) IBOutlet UITextField *passwdTF;
@end

@implementation LoginViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (IBAction)login {
    //NSDictionary *dic = [NSDictionary dictionaryWithObjects:@[@"runnphoenix",@"runn2reborngc"] forKeys:@[@"username",@"password"]];
    //NSURL *url = [NSURL URLWithString:@"https://gtdcomplete-171902.appspot.com/login.json"];
    NSDictionary *dic = [NSDictionary dictionaryWithObjects:@[self.nameTF.text, self.passwdTF.text] forKeys:@[@"username",@"password"]];
    NSURL *url = [NSURL URLWithString:@"http://localhost:8080/login.json"];
    NSData *jsonData = [NSJSONSerialization dataWithJSONObject:dic options:NSJSONWritingPrettyPrinted error:nil];
    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
    [request setHTTPMethod:@"POST"];
    [request setHTTPBody:jsonData];
    NSURLSession *session = [NSURLSession sharedSession];
    NSURLSessionDataTask *task = [session dataTaskWithRequest:request
                                            completionHandler:^(NSData * _Nullable data, NSURLResponse * _Nullable response, NSError * _Nullable error) {
                                                NSString *str = [[NSString alloc]initWithData:data encoding:NSUTF8StringEncoding];
                                                NSLog(@"%@",str);
                                                NSDictionary *jsonDic = [NSJSONSerialization JSONObjectWithData:data options:NSJSONReadingAllowFragments error:nil];
                                                NSString *errorMessage = [jsonDic objectForKey:@"error"];
                                                if(errorMessage == nil){
                                                    NSString *user_id = [jsonDic objectForKey:@"uid"];
                                                    NSString *user_name = [jsonDic objectForKey:@"uname"];
                                                    NSLog(@"%@",user_id);
                                                    NSLog(@"%@",user_name);
                                                    [[NSUserDefaults standardUserDefaults] setObject:user_id forKey:@"uid"];
                                                    [[NSUserDefaults standardUserDefaults] setObject:user_name forKey:@"uname"];
                                                    // 跳转到用户页面
                                                    NSLog(@"xxxxxxx");
                                                    [self.navigationController popToRootViewControllerAnimated:YES];
                                                }else{
                                                    // 显示错误信息
                                                }
                                            }];
    [task resume];
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
