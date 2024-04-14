resource "aws_launch_template" "wordpress" {
  name_prefix            = "wordpress-launch-template-"
  image_id               = var.ami_id
  instance_type          = var.instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [module.vpc.default_security_group_id]
  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "wordpress"
    }
  }
}

resource "aws_autoscaling_group" "wordpress_asg" {
  launch_template {
    id      = aws_launch_template.wordpress.id
    version = "$Latest"
  }

  vpc_zone_identifier = module.vpc.private_subnets
  min_size            = 1
  max_size            = 10

  #target_group_arns = [aws_lb_target_group.app.arn]

  tag {
    key                 = "Name"
    value               = "wordpress"
    propagate_at_launch = true
  }
}

resource "aws_autoscaling_policy" "app_cpu_tracking" {
  name                      = "cpu-utilization-tracking"
  policy_type               = "TargetTrackingScaling"
  autoscaling_group_name    = aws_autoscaling_group.wordpress_asg.name
  estimated_instance_warmup = 300

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }

    target_value = 70.0
  }
}

resource "aws_lb" "wordpress_lb" {
  name               = "wordpress-lb"
  load_balancer_type = "application"
  subnets            = module.vpc.public_subnets
}

resource "aws_lb_target_group" "wordpress" {
  name     = "wordpress-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = module.vpc.vpc_id

  health_check {
    enabled             = true
    interval            = 30
    path                = "/"
    protocol            = "HTTP"
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
    matcher             = "200"
  }
}

resource "aws_lb_listener" "wordpress" {
  load_balancer_arn = aws_lb.wordpress_lb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.wordpress.arn
  }
}
