"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
var google_auth_library_1 = require("google-auth-library");
var google_auth_library_2 = require("google-auth-library");
var iap_client = {
    id: "279793202318-qthcho2scvefo0mse11giihlpesdcprg.apps.googleusercontent.com",
    secret: "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",
    redirect: "https://iap.googleapis.com/v1/oauth/clientIds/279793202318-qthcho2scvefo0mse11giihlpesdcprg.apps.googleusercontent.com:handleRedirect",
    audience: "/projects/279793202318/global/backendServices/1262922268840097096",
};
var url = "https://deploy-staging.getsentry.net/go/api/current_user";
var GOCD_TOKEN = "5e838e80c9409d5b8e3f4cc0170860c24761b170";
function main3() {
    return __awaiter(this, void 0, void 0, function () {
        var auth, client, _a, _b;
        return __generator(this, function (_c) {
            switch (_c.label) {
                case 0:
                    auth = new google_auth_library_1.GoogleAuth({
                        scopes: "https://www.googleapis.com/auth/cloud-platform",
                    });
                    return [4 /*yield*/, auth.getClient()];
                case 1:
                    client = _c.sent();
                    _b = (_a = console).log;
                    return [4 /*yield*/, client.getRequestHeaders()];
                case 2:
                    _b.apply(_a, [_c.sent()]);
                    return [2 /*return*/];
            }
        });
    });
}
function main4() {
    return __awaiter(this, void 0, void 0, function () {
        var auth2, client2, res;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    auth2 = new google_auth_library_1.GoogleAuth({
                        scopes: ["https://www.googleapis.com/auth/cloud-platform"],
                        clientOptions: {
                            clientId: iap_client.id,
                            clientSecret: iap_client.secret,
                            redirectUri: iap_client.redirect,
                        },
                    });
                    return [4 /*yield*/, auth2.getIdTokenClient(iap_client.audience)];
                case 1:
                    client2 = _a.sent();
                    return [4 /*yield*/, client2.request({ url: url })];
                case 2:
                    res = _a.sent();
                    console.log(res.data);
                    return [2 /*return*/];
            }
        });
    });
}
function main() {
    return __awaiter(this, void 0, void 0, function () {
        var clientOptions, auth, client, id_client, res;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    clientOptions = {
                        clientId: iap_client.id,
                        clientSecret: iap_client.secret,
                        redirectUri: iap_client.redirect,
                    };
                    auth = new google_auth_library_1.GoogleAuth({
                        scopes: ["https://www.googleapis.com/auth/cloud-platform"],
                        clientOptions: clientOptions,
                    });
                    return [4 /*yield*/, auth.getApplicationDefaultAsync(clientOptions)];
                case 1:
                    client = _a.sent();
                    id_client = new google_auth_library_2.IdTokenClient({
                        targetAudience: iap_client.audience,
                        idTokenProvider: client,
                    });
                    return [4 /*yield*/, id_client.request({ url: url })];
                case 2:
                    res = _a.sent();
                    console.log(res.data);
                    return [2 /*return*/];
            }
        });
    });
}
main().catch(console.error);
