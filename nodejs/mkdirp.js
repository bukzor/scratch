var path = require('path');
var fs = require('fs');

function mkdirp (p, f, made) {
    if (!made) made = null;

    var cb = f || function () {};
    p = path.resolve(p);

    fs.mkdir(p, function (er) {
        if (!er) {
            made = made || p;
            return cb(null, made);
        }
        switch (er.code) {
            case 'ENOENT':
                mkdirp(path.dirname(p), function (er, made) {
                    if (er) cb(er, made);
                    else mkdirp(p, cb, made);
                });
                break;

                // In the case of any other error, just see if there's a dir
                // there already.  If so, then hooray!  If not, then something
                // is borked.
            default:
                fs.stat(p, function (er2, stat) {
                    // if the stat fails, then that's super weird.
                    // let the original error be the failure reason.
                    if (er2 || !stat.isDirectory()) cb(er, made)
                    else cb(null, made);
                });
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
