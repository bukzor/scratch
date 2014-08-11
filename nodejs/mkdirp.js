var path = require('path');
var fs = require('fs');

function mkdirp (p, cb) {
    cb = cb || function () {};
    p = path.resolve(p);

    fs.mkdir(p, function (er) {
        if (!er) {
            return cb(null);
        }
        switch (er.code) {
            case 'ENOENT':
                // The directory doesn't exist. Make its parent and try again.
                mkdirp(path.dirname(p), function (er) {
                    if (er) cb(er);
                    else mkdirp(p, cb);
                });
                break;

                // In the case of any other error, something is borked.
            default:
                cb(er);
                break;
        }
    });
}



var main = function(){
    process.argv.slice(2).forEach(function(val, index, array) {
        mkdirp(val);
    })
}

if (require.main === module) {
    main();
}
