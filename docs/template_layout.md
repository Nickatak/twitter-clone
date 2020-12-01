### Template inheritance layout (INC)
In the case that you're working on a template and need to alter something further up the heirarchy chain.

```
base.html
├── auth/index.html
├── auth/login.html
├── auth/signup.html
└── twitter/navbar.html
    ├── twitter/dashboard.html
    └── twitter/profile.html
```