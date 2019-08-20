//
//  ViewController.m
//  TMConfuse
//
//  Created by wuaming on 2018/4/3.
//  Copyright © 2018年 tim. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()
///懒加载property测试
@property (nonatomic, strong) NSMutableArray *testArray;
@property (nonatomic, retain) UITableViewCell *inviteCell;  // Invite outside

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];

}

- (void)function1 {

}

- (void)Function1 {

}

- (NSString *)function2 {
    return @"text";
}

- (void)ignoreTestFunction {

}

- (void)ignoreFunction2:(NSString *)text {

}

- (void)functionWithTitle:(NSString *)title subTitle:(NSString *)subTitle {

}

#pragma mark - 懒加载

- (NSMutableArray *)testArray {
    if (!_testArray) {
        _testArray = [NSMutableArray array];
    }
    return _testArray;
}

- (UITableViewCell*)inviteCell
{
    if (!_inviteCell)
    {
        _inviteCell = [[UITableViewCell alloc] initWithStyle: UITableViewCellStyleDefault reuseIdentifier:nil];
        
        _inviteCell.textLabel.text = NSLocalizedString(@"Members in your organization only", @"");
    }
    
    return _inviteCell;
}


@end
