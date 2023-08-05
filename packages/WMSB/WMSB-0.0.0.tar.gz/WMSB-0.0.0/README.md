# West's Message Service Bus

The purpose of this package, and the service that powers it, is to enable anyone, regardless of what caliber
programmer they are, to write scripts that can share live data over the internet.

The primary features are:

 - No server has to be run or created by the user.
 - The module's interface is similar to a dict.
 - There is a reasonable level of security.
 - Setup takes less than 5 minutes and involves making an account and copy pasting a string token.
 - A data hierarchy of **Name Space** > **Mapping** > **Item** (Mappings can be interfaced with like a dict via this module)

## Notes

### Security

#### Risks
This package, optionally, uses the Pickle module or repr builtin function in a very insecure way. Use this module
at your own risk.

#### Ways to use safely
 - Using a private name space and not sharing tokens that can access that namespace.
 - Use the default filter class or write your own. The best option would be to use JSON serialization. Or
pickle with some way to check for tampering.
 - Hold Locks on data that you do not want to be changed.

### Service Access
You can register to create your own tokens and Name Spaces at [West's Network](https://westd.dev).

The Service is in a very early alpha state. Your registration must be manually reviewed before you will be
verified to access the service. It is the reviewer's discretion whether or not you will be verified. You may
not create or manage tokens until your account is verified. However, there is a Demo Token that you can use
in the meantime.

#### Demo Token
The demo token that is used by the examples can only access the shared Name Space and may be revoked at any
time.


