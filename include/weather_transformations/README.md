Welcome to your new dbt project!

### Snowflake setup

dbt uses the `weather_transformations` profile from
`C:\Users\<your-user>\.dbt\profiles.yml`. The profile is configured for the
Snowflake account used by the loader and reads the password from the
`SNOWFLAKE_PASSWORD` environment variable.

In PowerShell, set the password for the current terminal session before
running dbt. `Get-Credential` prompts without echoing the password:

```powershell
$credential = Get-Credential -UserName your_username -Message "Snowflake credentials"
$env:SNOWFLAKE_PASSWORD = $credential.GetNetworkCredential().Password
dbt debug
```

If you open a new terminal, set the variable again or configure it in your
user environment. Do not put the password in this repository or commit
`profiles.yml` to source control.

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
