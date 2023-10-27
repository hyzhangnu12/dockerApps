const mongoose = require('mongoose');
async function run() {
    await mongoose.connect('mongodb://127.0.0.1:27017/mydb', {
        useNewUrlParser: true,
        useUnifiedTopology: true,
        "auth": {
            "authSource": "admin"
        },
        "user": "root",
        "pass": "password"
    });
    
    const Blog = await mongoose.model('blogs', { title: String, content: String})

    for (var i = 1; i <= 10; i++) {
        var blog = new Blog({ title: "my-blog-" + i, content: "Hello, Moto!"})
        await blog.save()
        console.log(`Done: {i}.`)
    }
    ProcessingInstruction.exit(0);
}

run();9