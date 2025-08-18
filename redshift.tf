resource "aws_redshiftserverless_namespace" "ns" {
  namespace_name      = "sales-namespace"
  admin_username      = "admin"
  admin_user_password = "kalyan"
  iam_roles           = [aws_iam_role.redshift_role.arn]
}

resource "aws_redshiftserverless_workgroup" "wg" {
  workgroup_name = "sales-workgroup"
  namespace_name = aws_redshiftserverless_namespace.ns.namespace_name
}

