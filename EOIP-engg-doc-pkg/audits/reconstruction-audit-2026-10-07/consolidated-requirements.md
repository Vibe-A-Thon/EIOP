# Consolidated Requirements For EOIP / KnowGridFlow Reconstruction

Generated: 2026-10-07 14:02:13Z

## Audit Position

This document is a reconstruction-grade consolidation of the project Markdown corpus plus the two supplied coverage audit JSON files. It is intentionally evidence-first: coverage JSON rows are recorded as coverage evidence, not as independent proof that every runtime behavior is production hardened.

The project-authored Markdown corpus was read line-by-line from the normal project file set returned by `rg --files -g "*.md"`. In addition, the generator read and hashed every Markdown file physically present under the workspace, excluding only `.git` and this generated output directory, so dependency/cache/test-fixture Markdown is inventoried without being promoted to product requirements.

## Corpus Coverage

| Metric | Value |
| --- | --- |
| Workspace Markdown files read | 818 |
| Workspace Markdown lines read | 112180 |
| Project Markdown files read | 184 |
| Project Markdown lines read | 30760 |
| Nonblank Markdown lines | 24577 |
| Requirement-like lines detected | 7509 |
| Status/gap/risk-like lines detected | 1600 |
| Requirement IDs in supplied audit JSON | 660 |

## Whole Workspace Markdown Inventory

This table accounts for every `.md` file under the workspace except `.git` internals and these generated reconstruction outputs. `Product source` means the file is part of the normal project corpus used for requirements; dependency/cache/test-fixture files are still read and hashed here but are not used as product requirements.

| Workspace Markdown file | Product source | Lines | SHA-256 prefix | First heading |
| --- | --- | --- | --- | --- |
| .pytest_cache/README.md | no | 8 | 420e808d79a6c25d | # pytest cache directory # |
| .venv/Lib/site-packages/fastapi/.agents/skills/fastapi/references/dependencies.md | no | 142 | 8b6b71a03fa14680 | # Dependency Injection |
| .venv/Lib/site-packages/fastapi/.agents/skills/fastapi/references/other-tools.md | no | 76 | a2c9199589027468 | # Other Tools |
| .venv/Lib/site-packages/fastapi/.agents/skills/fastapi/references/path-operations.md | no | 93 | ed8d2a21123bcf63 | # Path Operations and Routing |
| .venv/Lib/site-packages/fastapi/.agents/skills/fastapi/references/pydantic.md | no | 93 | 840ab962739861ae | # Pydantic |
| .venv/Lib/site-packages/fastapi/.agents/skills/fastapi/references/responses.md | no | 79 | 7c921508bbd09369 | # Responses |
| .venv/Lib/site-packages/fastapi/.agents/skills/fastapi/references/streaming.md | no | 105 | 6c76882a7c1b4e47 | # Streaming |
| .venv/Lib/site-packages/fastapi/.agents/skills/fastapi/SKILL.md | no | 332 | 0fc817d25584b489 | # FastAPI |
| .venv/Lib/site-packages/httpcore-1.0.9.dist-info/licenses/LICENSE.md | no | 27 | fdcb59154c74cbab | (no markdown heading) |
| .venv/Lib/site-packages/httpx-0.28.1.dist-info/licenses/LICENSE.md | no | 12 | 4ec59d544f12b5f5 | (no markdown heading) |
| .venv/Lib/site-packages/idna-3.20.dist-info/licenses/LICENSE.md | no | 31 | 1a9a4f0e3d479a27 | (no markdown heading) |
| .venv/Lib/site-packages/olefile/doc/API.md | no | 313 | c63c97b91409db1f | ## Test if a file is an OLE container |
| .venv/Lib/site-packages/olefile/doc/Contribute.md | no | 28 | 15fecea8048d9d6b | (no markdown heading) |
| .venv/Lib/site-packages/olefile/doc/Home.md | no | 94 | 650ad7a3b0b2048a | (no markdown heading) |
| .venv/Lib/site-packages/olefile/doc/Install.md | no | 37 | 861ed1d5e21a5aee | (no markdown heading) |
| .venv/Lib/site-packages/olefile/doc/License.md | no | 54 | 17cc0185ea7dac96 | (no markdown heading) |
| .venv/Lib/site-packages/olefile/doc/OLE_Overview.md | no | 29 | a4e8b65096427264 | (no markdown heading) |
| .venv/Lib/site-packages/oletools-0.60.2.dist-info/LICENSE.md | no | 52 | 58a91c4cc6796214 | (no markdown heading) |
| .venv/Lib/site-packages/oletools/doc/Changelog.md | no | 216 | 6f6fac4f16296710 | (no markdown heading) |
| .venv/Lib/site-packages/oletools/doc/Contribute.md | no | 38 | a77d41bcff707ba4 | (no markdown heading) |
| .venv/Lib/site-packages/oletools/doc/formats_vs_techniques.md | no | 359 | f6803b0bc2da0e1a | # File formats, Techniques and Tools |
| .venv/Lib/site-packages/oletools/doc/Home.md | no | 78 | 8b5f8d9ba97926c8 | ### Tools to analyze malicious documents |
| .venv/Lib/site-packages/oletools/doc/Install.md | no | 180 | bf23ff48233a2d5a | ### Linux, Mac OSX, Unix |
| .venv/Lib/site-packages/oletools/doc/License.md | no | 80 | 6f30b03d8776fbda | (no markdown heading) |
| .venv/Lib/site-packages/oletools/doc/mraptor.md | no | 112 | 006e66e06c05d0ca | ## Usage |
| .venv/Lib/site-packages/oletools/doc/msodde.md | no | 117 | 462579a96d1b7990 | ## References about DDE exploitation |
| .venv/Lib/site-packages/oletools/doc/olebrowse.md | no | 77 | d2a941e9a7edb2ca | (no markdown heading) |
| .venv/Lib/site-packages/oletools/doc/oledir.md | no | 66 | b6680c48aca3bde1 | ## Usage |
| .venv/Lib/site-packages/oletools/doc/oleid.md | no | 118 | e7555d75c1f47468 | ## Main Features |
| .venv/Lib/site-packages/oletools/doc/olemap.md | no | 55 | b21fbaa92e8bb488 | ## Usage |
| .venv/Lib/site-packages/oletools/doc/olemeta.md | no | 44 | d794090d0eeb4300 | ## Usage |
| .venv/Lib/site-packages/oletools/doc/oleobj.md | no | 45 | ed7860c81608f748 | ## Usage |
| .venv/Lib/site-packages/oletools/doc/oletimes.md | no | 73 | 993135985cfc114b | ## Usage |
| .venv/Lib/site-packages/oletools/doc/olevba.md | no | 556 | adeaa3c96496a7b2 | ## Supported formats |
| .venv/Lib/site-packages/oletools/doc/pyxswf.md | no | 98 | 180949871e91098d | ## Usage |
| .venv/Lib/site-packages/oletools/doc/rtfobj.md | no | 103 | cf1399a1de5e4736 | ## Usage |
| .venv/Lib/site-packages/pip-26.2.1.dist-info/licenses/src/pip/_vendor/idna/LICENSE.md | no | 31 | 1a9a4f0e3d479a27 | (no markdown heading) |
| .venv/Lib/site-packages/pip/_vendor/idna/LICENSE.md | no | 31 | 1a9a4f0e3d479a27 | (no markdown heading) |
| .venv/Lib/site-packages/pyparsing/ai/best_practices.md | no | 75 | aa53ca4e67931186 | ## Planning |
| .venv/Lib/site-packages/respx-0.23.1.dist-info/LICENSE.md | no | 29 | 741b7f3f139d58c8 | (no markdown heading) |
| .venv/Lib/site-packages/soupsieve-2.10.dist-info/licenses/LICENSE.md | no | 21 | 76a0acdb98c3a636 | (no markdown heading) |
| .venv/Lib/site-packages/starlette-1.7.0.dist-info/licenses/LICENSE.md | no | 27 | dcb95677a0224024 | (no markdown heading) |
| .venv/Lib/site-packages/uvicorn-0.54.0.dist-info/licenses/LICENSE.md | no | 27 | efe1acf3e62fb99c | (no markdown heading) |
| .venv/Lib/site-packages/win32comext/mapi/NOTICE.md | no | 6 | dedf997c8f5568a0 | # Licensing |
| agent_runbook.md | yes | 83 | 0e916fd7a4cf5e61 | # EOIP Agent Runbook |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/css-language-features/README.md | no | 9 | feb72f87e9b92c66 | # Language Features for CSS, SCSS, and LESS files |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/emmet/README.md | no | 9 | 4efc8fbae707e94f | # Emmet integration in Visual Studio Code |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/git-base/README.md | no | 21 | 513ac49d715d48b6 | # Git static contributions and remote repository picker |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/git/README.md | no | 26 | c818d12a05ed61d1 | # Git integration for Visual Studio Code |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/github-authentication/README.md | no | 7 | 21979ad332da7268 | # GitHub Authentication for Visual Studio Code |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/github/README.md | no | 12 | bfc700cc6d369f19 | # GitHub for Visual Studio Code |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/github/testWorkspace/docs/PULL_REQUEST_TEMPLATE.md | no | 0 | e3b0c44298fc1c14 | (no markdown heading) |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/github/testWorkspace/docs/PULL_REQUEST_TEMPLATE/a.md | no | 0 | e3b0c44298fc1c14 | (no markdown heading) |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/github/testWorkspace/docs/PULL_REQUEST_TEMPLATE/b.md | no | 0 | e3b0c44298fc1c14 | (no markdown heading) |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/github/testWorkspace/PULL_REQUEST_TEMPLATE.md | no | 0 | e3b0c44298fc1c14 | (no markdown heading) |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/github/testWorkspace/PULL_REQUEST_TEMPLATE/a.md | no | 0 | e3b0c44298fc1c14 | (no markdown heading) |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/github/testWorkspace/PULL_REQUEST_TEMPLATE/b.md | no | 0 | e3b0c44298fc1c14 | (no markdown heading) |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/github/testWorkspace/some-markdown.md | no | 0 | e3b0c44298fc1c14 | (no markdown heading) |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/grunt/README.md | no | 13 | 132d630a33b30f47 | # Grunt - The JavaScript Task Runner |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/gulp/README.md | no | 13 | fd20f9d9c0e84697 | # Gulp - Automate and enhance your workflow |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/html-language-features/README.md | no | 9 | 8e4b0b15c79dea79 | # Language Features for HTML |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/ipynb/README.md | no | 9 | bcd0f696c89ed229 | # Jupyter for Visual Studio Code |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/jake/README.md | no | 13 | 03d0a0f9f2958935 | # Jake - JavaScript build tool |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/json-language-features/README.md | no | 7 | eb4cb0f084fc44d2 | # Language Features for JSON files |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/markdown-language-features/README.md | no | 7 | 1a279d135194cb27 | # Language Features for Markdown files |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/markdown-math/README.md | no | 5 | 581b1b773dc1a474 | # Markdown Math |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/media-preview/README.md | no | 28 | 31a85a73367039cc | # Media Preview |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/merge-conflict/README.md | no | 7 | 0949241390b99786 | # Merge Conflict |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/microsoft-authentication/README.md | no | 9 | e15214758c01431e | # Microsoft Authentication for Visual Studio Code |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/ms-vscode.js-debug-companion/README.md | no | 7 | 77d796f0123b7b55 | # js-debug-companion |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/ms-vscode.js-debug-companion/SECURITY.md | no | 41 | c97a57b6770b3c81 | ## Security |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/ms-vscode.js-debug/readme.md | no | 134 | a85db1a8f7c0f92b | ## Usage |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/ms-vscode.vscode-js-profile-table/README.md | no | 9 | 581d187c03db9a71 | # `vscode-js-profile-table` |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/notebook-renderers/README.md | no | 9 | 908a499d6a9cd4bd | # Builtin Notebook Output Renderers for Visual Studio Code |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/npm/README.md | no | 42 | fc7c444050c2d0ae | # Node npm |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/php-language-features/README.md | no | 7 | 98c0d45414732f6c | # Language Features for PHP files |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/references-view/README.md | no | 34 | 719851afe526e019 | # References View |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/search-result/README.md | no | 5 | c68a718466ecefb7 | # Language Features for Search Result files |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/simple-browser/README.md | no | 5 | f999bf42b9bd681f | # Simple Browser |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/terminal-suggest/README.md | no | 7 | 5d037e2b924fe07d | # Terminal Suggestions |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/theme-seti/README.md | no | 32 | d0c331acc0dd884e | # theme-seti |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/extensions/typescript-language-features/README.md | no | 7 | b78ddba95a903828 | # Language Features for TypeScript and JavaScript files |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/@microsoft/1ds-core-js/SECURITY.md | no | 41 | dd0376320839eaab | ## Security |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/@microsoft/1ds-post-js/SECURITY.md | no | 41 | dd0376320839eaab | ## Security |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/@microsoft/applicationinsights-core-js/dist/applicationinsights-core-js.api.md | no | 1358 | 0a8ccf1f399e2064 | ## API Report File for "@microsoft/applicationinsights-core-js" |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/@microsoft/dynamicproto-js/RELEASES.md | no | 124 | 542b72f221c93760 | # Releases |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/@microsoft/dynamicproto-js/SECURITY.md | no | 41 | dd0376320839eaab | ## Security |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/@vscode/deviceid/SECURITY.md | no | 41 | 891c6326bdd8ea02 | ## Security |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/@vscode/proxy-agent/LICENSE.md | no | 24 | 22a11dae36edebdc | (no markdown heading) |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/@vscode/proxy-agent/SECURITY.md | no | 41 | 430987b8c5f30c36 | ## Security |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/@vscode/ripgrep/SECURITY.md | no | 41 | ca6b94724f2c1e72 | ## Security |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/@vscode/spdlog/SECURITY.md | no | 41 | 430987b8c5f30c36 | ## Security |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/@vscode/tree-sitter-wasm/SECURITY.md | no | 41 | 7b6976eec43edfa6 | ## Security |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/@vscode/vscode-languagedetection/SECURITY.md | no | 41 | 830e94b83c3b6f45 | ## Security |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/@vscode/windows-mutex/SECURITY.md | no | 41 | 985e3fc1a4c6591e | ## Security |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/@vscode/windows-process-tree/SECURITY.md | no | 41 | dd0376320839eaab | ## Security |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/@vscode/windows-registry/SECURITY.md | no | 41 | 985e3fc1a4c6591e | ## Security |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/bindings/LICENSE.md | no | 22 | 85fde19744c84cfa | (no markdown heading) |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/bl/LICENSE.md | no | 13 | 9377db95383c8bef | (no markdown heading) |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/buffer/AUTHORS.md | no | 70 | c30faf5cc3be9f99 | # Authors |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/chrome-remote-interface/node_modules/commander/Readme.md | no | 351 | 34ee3375994baeb6 | # Commander.js |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/font-finder/LICENSE.md | no | 21 | 5c15db361b74f2f3 | (no markdown heading) |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/font-ligatures/LICENSE.md | no | 21 | 5c15db361b74f2f3 | (no markdown heading) |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/get-system-fonts/LICENSE.md | no | 21 | 5c15db361b74f2f3 | (no markdown heading) |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/js-base64/LICENSE.md | no | 27 | fcf06aacb36ee292 | (no markdown heading) |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/kerberos/HISTORY.md | no | 228 | 71727eccba7cc614 | # Changelog |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/ms/license.md | no | 21 | 6652830c2607c722 | (no markdown heading) |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/napi-build-utils/index.md | no | 81 | 3edaf008baa77c71 | ## napi-build-utils |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/native-keymap/SECURITY.md | no | 41 | 81ed58e26769508d | ## Security |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/native-watchdog/SECURITY.md | no | 41 | 81ed58e26769508d | ## Security |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/opentype.js/AUTHORS.md | no | 36 | 064eaeb01dd240df | (no markdown heading) |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/opentype.js/RELEASES.md | no | 171 | 8f1ce5ea64c88d9e | (no markdown heading) |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/promise-stream-reader/LICENSE.md | no | 21 | 5c15db361b74f2f3 | (no markdown heading) |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/readable-stream/GOVERNANCE.md | no | 136 | 7a521e462d1c6f3b | ### Streams Working Group |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/sprintf-js/CONTRIBUTORS.md | no | 26 | 63258da288e3a6e6 | (no markdown heading) |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/tslib/SECURITY.md | no | 41 | 89c4e4b9ba7ec705 | ## Security |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/uuid/LICENSE.md | no | 9 | beaa6b04fb82e41d | (no markdown heading) |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/vscode-oniguruma/SECURITY.md | no | 41 | 81ed58e26769508d | ## Security |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/vscode-textmate/LICENSE.md | no | 21 | b5cb7ff7859e7d28 | (no markdown heading) |
| apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/resources/app/node_modules/vscode-textmate/SECURITY.md | no | 41 | 81ed58e26769508d | ## Security |
| apps/vscode-extension/node_modules/@azu/format-text/README.md | no | 23 | 987d9662e4004ed6 | ## @azu/format-text |
| apps/vscode-extension/node_modules/@azu/style-format/README.md | no | 30 | 6417a11ae004a2ad | ## style-format |
| apps/vscode-extension/node_modules/@azure/abort-controller/README.md | no | 83 | 8f9d944e43d7f83c | # Azure Abort Controller client library for JavaScript |
| apps/vscode-extension/node_modules/@azure/core-auth/README.md | no | 79 | a2ea5ceddb901723 | # Azure Core Authentication client library for JavaScript |
| apps/vscode-extension/node_modules/@azure/core-client/README.md | no | 50 | 6d2f44e2d8239620 | # Azure Core Service client library for JavaScript |
| apps/vscode-extension/node_modules/@azure/core-process/CHANGELOG.md | no | 7 | d07c83329d372f2c | # Release History |
| apps/vscode-extension/node_modules/@azure/core-process/README.md | no | 68 | e95e1b467b925537 | # Azure Core Process client library for JavaScript |
| apps/vscode-extension/node_modules/@azure/core-rest-pipeline/README.md | no | 176 | 97bfe860db008086 | # Azure Core HTTP client library for JavaScript |
| apps/vscode-extension/node_modules/@azure/core-tracing/README.md | no | 35 | c8b90ffba53781c9 | # Azure Core tracing library for JavaScript |
| apps/vscode-extension/node_modules/@azure/core-util/README.md | no | 38 | b6f456b8db8e4f81 | # Azure Core Util client library for JavaScript (Experimental) |
| apps/vscode-extension/node_modules/@azure/identity/README.md | no | 378 | f47a40432a40ff56 | # Azure Identity client library for JavaScript |
| apps/vscode-extension/node_modules/@azure/logger/README.md | no | 122 | a4812e1fca0e837c | # Azure Logger client library for JavaScript |
| apps/vscode-extension/node_modules/@azure/msal-browser/README.md | no | 175 | e97ce1466bddf95c | # Microsoft Authentication Library for JavaScript (MSAL.js) for Browser-Based Single-Page Applications |
| apps/vscode-extension/node_modules/@azure/msal-browser/scripts/README.md | no | 112 | d139d11e60cccf1e | # MSAL Browser Log Decoder |
| apps/vscode-extension/node_modules/@azure/msal-common/browser/README.md | no | 1 | ae65f19e4da9c00c | (no markdown heading) |
| apps/vscode-extension/node_modules/@azure/msal-common/node/README.md | no | 1 | ae65f19e4da9c00c | (no markdown heading) |
| apps/vscode-extension/node_modules/@azure/msal-common/README.md | no | 53 | b1b1ca07d2aa11d2 | # Microsoft Authentication Library for JavaScript (MSAL.js) Common Protocols Package |
| apps/vscode-extension/node_modules/@azure/msal-node/README.md | no | 194 | 8870281e75c52f82 | # Microsoft Authentication Library for Node (msal-node) |
| apps/vscode-extension/node_modules/@babel/code-frame/README.md | no | 19 | c8695ddb503d13b5 | # @babel/code-frame |
| apps/vscode-extension/node_modules/@babel/helper-validator-identifier/README.md | no | 19 | 42b17e7ea124f565 | # @babel/helper-validator-identifier |
| apps/vscode-extension/node_modules/@isaacs/cliui/LICENSE.md | no | 63 | c58416e852f7603c | # Blue Oak Model License |
| apps/vscode-extension/node_modules/@isaacs/cliui/README.md | no | 151 | 0647da36ad7d91f5 | # @isaacs/cliui |
| apps/vscode-extension/node_modules/@nodelib/fs.scandir/README.md | no | 171 | 1fb8cfd1e8d2ed3a | # @nodelib/fs.scandir |
| apps/vscode-extension/node_modules/@nodelib/fs.stat/README.md | no | 126 | 1003c9d5c66b3933 | # @nodelib/fs.stat |
| apps/vscode-extension/node_modules/@nodelib/fs.walk/README.md | no | 215 | 584b8555ea714e8d | # @nodelib/fs.walk |
| apps/vscode-extension/node_modules/@secretlint/config-creator/README.md | no | 44 | 0249341309f0aac4 | # @secretlint/config-creator |
| apps/vscode-extension/node_modules/@secretlint/config-loader/README.md | no | 102 | 3f65348d4ebcba54 | # @secretlint/config-loader |
| apps/vscode-extension/node_modules/@secretlint/core/README.md | no | 47 | 52d47cfd5710096e | # @secretlint/core |
| apps/vscode-extension/node_modules/@secretlint/formatter/node_modules/chalk/readme.md | no | 297 | 03d260b86ecf3bec | ## Info |
| apps/vscode-extension/node_modules/@secretlint/formatter/README.md | no | 48 | 89b3d60534bc623a | # @secretlint/formatter |
| apps/vscode-extension/node_modules/@secretlint/node/README.md | no | 65 | 593c31e5f7129b05 | # @secretlint/node |
| apps/vscode-extension/node_modules/@secretlint/profiler/README.md | no | 44 | f14d4935e7b6798c | # @secretlint/profiler |
| apps/vscode-extension/node_modules/@secretlint/resolver/README.md | no | 46 | c905ab720827470b | # @secretlint/resolver |
| apps/vscode-extension/node_modules/@secretlint/secretlint-formatter-sarif/README.md | no | 47 | d0ce7389b205368a | # @secretlint/secretlint-formatter-sarif |
| apps/vscode-extension/node_modules/@secretlint/secretlint-rule-no-dotenv/README.md | no | 56 | 485c5bdc6c5a0f4a | # @secretlint/secretlint-rule-no-dotenv |
| apps/vscode-extension/node_modules/@secretlint/secretlint-rule-preset-recommend/README.md | no | 121 | 4673e4c82604ef1c | # @secretlint/secretlint-rule-preset-recommend |
| apps/vscode-extension/node_modules/@secretlint/source-creator/README.md | no | 51 | 7c107ec5259a21bb | # @secretlint/source-creator |
| apps/vscode-extension/node_modules/@secretlint/types/README.md | no | 44 | b33c2ead9f9d4d26 | # @secretlint/types |
| apps/vscode-extension/node_modules/@sindresorhus/merge-streams/readme.md | no | 53 | 0d4eab59e22da7f7 | # merge-streams |
| apps/vscode-extension/node_modules/@textlint/ast-node-types/README.md | no | 65 | eb2bc76c8c1c7ba5 | # @textlint/ast-node-types |
| apps/vscode-extension/node_modules/@textlint/linter-formatter/node_modules/ansi-regex/readme.md | no | 78 | 3ebc0f845b1bab50 | # ansi-regex |
| apps/vscode-extension/node_modules/@textlint/linter-formatter/node_modules/pluralize/Readme.md | no | 78 | 3b00c194d0f37370 | # Pluralize |
| apps/vscode-extension/node_modules/@textlint/linter-formatter/node_modules/strip-ansi/readme.md | no | 46 | cb384db30337ecec | # strip-ansi [![Build Status](https://travis-ci.org/chalk/strip-ansi.svg?branch=master)](https://travis-ci.org/chalk/strip-ansi) |
| apps/vscode-extension/node_modules/@textlint/linter-formatter/README.md | no | 92 | 5b89768466048f75 | # @textlint/linter-formatter |
| apps/vscode-extension/node_modules/@textlint/module-interop/README.md | no | 94 | 33a9f09133c5ac34 | # @textlint/module-interop |
| apps/vscode-extension/node_modules/@textlint/resolver/README.md | no | 46 | 02b654c999bc9a45 | # @textlint/resolver |
| apps/vscode-extension/node_modules/@textlint/types/README.md | no | 106 | 72159cec357e13e5 | # @textlint/types |
| apps/vscode-extension/node_modules/@types/normalize-package-data/README.md | no | 62 | 8d4b5cf6d9d5094c | # Installation |
| apps/vscode-extension/node_modules/@types/sarif/README.md | no | 15 | 5982728e9849f8a0 | # Installation |
| apps/vscode-extension/node_modules/@typespec/ts-http-runtime/README.md | no | 177 | e2a8ad82c942808d | # ts-http-runtime |
| apps/vscode-extension/node_modules/@vscode/test-electron/CHANGELOG.md | no | 285 | 805cb556660af824 | # Changelog |
| apps/vscode-extension/node_modules/@vscode/test-electron/README.md | no | 147 | 02e4cc21e1df5c5f | # vscode-test |
| apps/vscode-extension/node_modules/@vscode/test-electron/SECURITY.md | no | 41 | 1dc0ed8d28b327cd | ## Security |
| apps/vscode-extension/node_modules/@vscode/vsce-sign/CODE_OF_CONDUCT.md | no | 9 | 9daeae709a0bd71b | # Microsoft Open Source Code of Conduct |
| apps/vscode-extension/node_modules/@vscode/vsce-sign/README.md | no | 25 | cc5abbd565336141 | # Visual Studio Code Extension Signing Tool Node.js module (@vscode/vsce-sign) |
| apps/vscode-extension/node_modules/@vscode/vsce-sign/SUPPORT.md | no | 25 | ec361acfa66edd85 | # TODO: The maintainer of this repo has not yet edited this file |
| apps/vscode-extension/node_modules/@vscode/vsce/README.md | no | 82 | 8bfa690c8c77902c | # @vscode/vsce |
| apps/vscode-extension/node_modules/agent-base/README.md | no | 69 | dc8148b1d0bbb80f | ### Turn a function into an [`http.Agent`][http.Agent] instance |
| apps/vscode-extension/node_modules/ajv/README.md | no | 207 | 38d924524762b917 | # Ajv JSON schema validator |
| apps/vscode-extension/node_modules/ansi-escapes/readme.md | no | 296 | b5fed27f37b6cdb1 | # ansi-escapes |
| apps/vscode-extension/node_modules/ansi-regex/readme.md | no | 66 | 58e5913e1fca8c33 | # ansi-regex |
| apps/vscode-extension/node_modules/ansi-styles/readme.md | no | 152 | 5331953ca5464ee0 | # ansi-styles [![Build Status](https://travis-ci.org/chalk/ansi-styles.svg?branch=master)](https://travis-ci.org/chalk/ansi-styles) |
| apps/vscode-extension/node_modules/argparse/CHANGELOG.md | no | 216 | c3f89be070b29b2d | # Changelog |
| apps/vscode-extension/node_modules/argparse/README.md | no | 84 | 44161d4e4baf71c7 | #!/usr/bin/env node |
| apps/vscode-extension/node_modules/astral-regex/readme.md | no | 46 | db798f6d4d4c17a7 | # astral-regex [![Build Status](https://travis-ci.org/kevva/astral-regex.svg?branch=master)](https://travis-ci.org/kevva/astral-regex) |
| apps/vscode-extension/node_modules/asynckit/README.md | no | 233 | be5bbf9c6a02774a | # asynckit [![NPM Module](https://img.shields.io/npm/v/asynckit.svg?style=flat)](https://www.npmjs.com/package/asynckit) |
| apps/vscode-extension/node_modules/azure-devops-node-api/README.md | no | 165 | 015bcc5915099c07 | # Azure DevOps Client for Node.js |
| apps/vscode-extension/node_modules/balanced-match/LICENSE.md | no | 21 | a1bd5deadb6a06dd | (no markdown heading) |
| apps/vscode-extension/node_modules/balanced-match/README.md | no | 97 | 428832d502fb64fc | # balanced-match |
| apps/vscode-extension/node_modules/base64-js/README.md | no | 34 | 057ef3ae4f4b4c9d | ## install |
| apps/vscode-extension/node_modules/binaryextensions/LICENSE.md | no | 101 | 5fdbfb4ce1eb9581 | # License |
| apps/vscode-extension/node_modules/binaryextensions/README.md | no | 199 | f17b2735549babca | # The Definitive List of Binary Extensions |
| apps/vscode-extension/node_modules/binaryextensions/SECURITY.md | no | 21 | 90fd67f751c47cfb | # Security Policy |
| apps/vscode-extension/node_modules/bl/LICENSE.md | no | 13 | 9377db95383c8bef | (no markdown heading) |
| apps/vscode-extension/node_modules/bl/README.md | no | 247 | 7569ad345a83c5bf | # bl *(BufferList)* |
| apps/vscode-extension/node_modules/boolbase/README.md | no | 10 | 9cac5bfc290d30cc | #boolbase |
| apps/vscode-extension/node_modules/boundary/README.md | no | 73 | 312c2140a9c1c9e0 | # boundary [![Actions Status: test](https://github.com/textlint/boundary/workflows/test/badge.svg)](https://github.com/textlint/boundary/actions?query=workflow%3A"test") |
| apps/vscode-extension/node_modules/brace-expansion/README.md | no | 151 | 0218f69610a394f4 | # brace-expansion |
| apps/vscode-extension/node_modules/braces/README.md | no | 586 | 947b0fc3cc12eaaa | # braces [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=W8YFZ425KND68) [![NPM version](https://img.shields.io/npm/v/braces.svg?style=flat)](https://www.npmjs.com/package/braces) [![NPM monthly downloads](https://img.shields.io/npm/dm/braces.svg?style=flat)](https://npmjs.org/package/braces) [![NPM total downloads](https://img.shields.io/npm/dt/braces.svg?style=flat)](https://npmjs.org/package/braces) [![Linux Build Status](https://img.shields.io/travis/micromatch/braces.svg?style=flat&label=Travis)](https://travis-ci.org/micromatch/braces) |
| apps/vscode-extension/node_modules/buffer-crc32/README.md | no | 47 | b71f8f946d623430 | # buffer-crc32 |
| apps/vscode-extension/node_modules/buffer-equal-constant-time/README.md | no | 50 | b4183b472a9f25b0 | # buffer-equal-constant-time |
| apps/vscode-extension/node_modules/buffer/AUTHORS.md | no | 70 | c30faf5cc3be9f99 | # Authors |
| apps/vscode-extension/node_modules/buffer/README.md | no | 410 | e45e1554755cf7f9 | # buffer [![travis][travis-image]][travis-url] [![npm][npm-image]][npm-url] [![downloads][downloads-image]][downloads-url] [![javascript style guide][standard-image]][standard-url] |
| apps/vscode-extension/node_modules/bundle-name/readme.md | no | 23 | 3945a5fadd54419b | # bundle-name |
| apps/vscode-extension/node_modules/call-bind-apply-helpers/CHANGELOG.md | no | 30 | 66327c6e1f42173b | # Changelog |
| apps/vscode-extension/node_modules/call-bind-apply-helpers/README.md | no | 62 | 9505a31673f63c1d | # call-bind-apply-helpers <sup>[![Version Badge][npm-version-svg]][package-url]</sup> |
| apps/vscode-extension/node_modules/call-bound/CHANGELOG.md | no | 42 | 333cf17d395a3c80 | # Changelog |
| apps/vscode-extension/node_modules/call-bound/README.md | no | 53 | 8c1e445125b01197 | # call-bound <sup>[![Version Badge][npm-version-svg]][package-url]</sup> |
| apps/vscode-extension/node_modules/chalk/readme.md | no | 341 | b93f6d0b7d7ae17c | ## Highlights |
| apps/vscode-extension/node_modules/cheerio-select/README.md | no | 18 | 127416834b91c0a8 | # cheerio-select [![NPM version](http://img.shields.io/npm/v/cheerio-select.svg)](https://npmjs.org/package/cheerio-select) [![Build Status](https://travis-ci.org/cheeriojs/cheerio-select.svg?branch=master)](http://travis-ci.org/cheeriojs/cheerio-select) [![Downloads](https://img.shields.io/npm/dm/cheerio-select.svg)](https://npmjs.org/package/cheerio-select) [![Coverage](https://coveralls.io/repos/cheeriojs/cheerio-select/badge.svg?branch=master)](https://coveralls.io/r/cheeriojs/cheerio-select) |
| apps/vscode-extension/node_modules/cheerio/Readme.md | no | 229 | e852d72500e5f39f | ## Installation |
| apps/vscode-extension/node_modules/chownr/README.md | no | 3 | cafe18aeaf5d10a5 | (no markdown heading) |
| apps/vscode-extension/node_modules/cli-cursor/readme.md | no | 39 | d258750206bc126c | # cli-cursor |
| apps/vscode-extension/node_modules/cli-spinners/readme.md | no | 54 | 78ea9628645750a0 | # cli-spinners |
| apps/vscode-extension/node_modules/cockatiel/readme.md | no | 1036 | 831e09d474ef22c6 | # Cockatiel |
| apps/vscode-extension/node_modules/color-convert/CHANGELOG.md | no | 54 | ee2ea4fe91d043ec | # 1.0.0 - 2016-01-07 |
| apps/vscode-extension/node_modules/color-convert/README.md | no | 68 | 8cb35dae3a64e6ed | # color-convert |
| apps/vscode-extension/node_modules/color-name/README.md | no | 11 | 796aef7006b975d2 | (no markdown heading) |
| apps/vscode-extension/node_modules/combined-stream/Readme.md | no | 138 | f4409df97c1568d7 | # combined-stream |
| apps/vscode-extension/node_modules/commander/Readme.md | no | 1157 | 34f5f0d63c641ea2 | # Commander.js |
| apps/vscode-extension/node_modules/core-util-is/README.md | no | 3 | 57072548a79553ec | # core-util-is |
| apps/vscode-extension/node_modules/cross-spawn/README.md | no | 89 | 022aa5bc5706ce14 | # cross-spawn |
| apps/vscode-extension/node_modules/css-select/README.md | no | 264 | e2b5ea08f820a02f | # css-select [![NPM version](http://img.shields.io/npm/v/css-select.svg)](https://npmjs.org/package/css-select) [![Build Status](https://travis-ci.com/fb55/css-select.svg?branch=master)](http://travis-ci.com/fb55/css-select) [![Downloads](https://img.shields.io/npm/dm/css-select.svg)](https://npmjs.org/package/css-select) [![Coverage](https://coveralls.io/repos/fb55/css-select/badge.svg?branch=master)](https://coveralls.io/r/fb55/css-select) |
| apps/vscode-extension/node_modules/css-what/readme.md | no | 69 | 9cd374c0fa2b825e | # css-what |
| apps/vscode-extension/node_modules/debug/README.md | no | 481 | 486cb669048bd501 | # debug |
| apps/vscode-extension/node_modules/decompress-response/readme.md | no | 48 | c0b4c1abab05fbf0 | # decompress-response [![Build Status](https://travis-ci.com/sindresorhus/decompress-response.svg?branch=master)](https://travis-ci.com/sindresorhus/decompress-response) |
| apps/vscode-extension/node_modules/deep-extend/CHANGELOG.md | no | 46 | aa675bee44b9c91c | (no markdown heading) |
| apps/vscode-extension/node_modules/deep-extend/README.md | no | 91 | 33132ea8c9f1f257 | (no markdown heading) |
| apps/vscode-extension/node_modules/default-browser-id/readme.md | no | 19 | d0858acce4213b4f | # default-browser-id |
| apps/vscode-extension/node_modules/default-browser/readme.md | no | 24 | 6ca3b4cda83d3c4d | # default-browser |
| apps/vscode-extension/node_modules/define-lazy-prop/readme.md | no | 55 | ff87272b6d459d12 | # define-lazy-prop |
| apps/vscode-extension/node_modules/delayed-stream/Readme.md | no | 141 | 5940dca6c65d1bf7 | # delayed-stream |
| apps/vscode-extension/node_modules/detect-libc/README.md | no | 163 | 51a97449c4438891 | # detect-libc |
| apps/vscode-extension/node_modules/dom-serializer/README.md | no | 109 | 0222b1ef9047b37b | # dom-serializer [![Build Status](https://travis-ci.com/cheeriojs/dom-serializer.svg?branch=master)](https://travis-ci.com/cheeriojs/dom-serializer) |
| apps/vscode-extension/node_modules/domelementtype/readme.md | no | 1 | 1eacf8172e22edf9 | (no markdown heading) |
| apps/vscode-extension/node_modules/domhandler/readme.md | no | 92 | afa440271734a494 | # domhandler [![Build Status](https://travis-ci.com/fb55/domhandler.svg?branch=master)](https://travis-ci.com/fb55/domhandler) |
| apps/vscode-extension/node_modules/domutils/readme.md | no | 31 | 7f67c7b54f6cd79a | # domutils [![Node.js CI](https://github.com/fb55/domutils/actions/workflows/nodejs-test.yml/badge.svg)](https://github.com/fb55/domutils/actions/workflows/nodejs-test.yml) |
| apps/vscode-extension/node_modules/dunder-proto/CHANGELOG.md | no | 24 | 889ec6c5fd3b8b18 | # Changelog |
| apps/vscode-extension/node_modules/dunder-proto/README.md | no | 54 | a04f8e67cb76f7d6 | # dunder-proto <sup>[![Version Badge][npm-version-svg]][package-url]</sup> |
| apps/vscode-extension/node_modules/ecdsa-sig-formatter/README.md | no | 65 | e4dbe1e1f6f54182 | # ecdsa-sig-formatter |
| apps/vscode-extension/node_modules/editions/LICENSE.md | no | 101 | 5fdbfb4ce1eb9581 | # License |
| apps/vscode-extension/node_modules/editions/README.md | no | 139 | 49817b2e6b23a9b5 | # editions |
| apps/vscode-extension/node_modules/editions/SECURITY.md | no | 21 | a8d2b64862575294 | # Security Policy |
| apps/vscode-extension/node_modules/emoji-regex/README.md | no | 73 | 83fa2a1a5a1dd731 | # emoji-regex [![Build status](https://travis-ci.org/mathiasbynens/emoji-regex.svg?branch=master)](https://travis-ci.org/mathiasbynens/emoji-regex) |
| apps/vscode-extension/node_modules/encoding-sniffer/README.md | no | 68 | 09e21a8fd5d8f266 | # encoding-sniffer [![Node.js CI](https://github.com/fb55/encoding-sniffer/actions/workflows/nodejs-test.yml/badge.svg)](https://github.com/fb55/encoding-sniffer/actions/workflows/nodejs-test.yml) |
| apps/vscode-extension/node_modules/end-of-stream/README.md | no | 54 | 177b2368d761e707 | # end-of-stream |
| apps/vscode-extension/node_modules/entities/readme.md | no | 122 | c0df24c407b69624 | # entities [![NPM version](https://img.shields.io/npm/v/entities.svg)](https://npmjs.org/package/entities) [![Downloads](https://img.shields.io/npm/dm/entities.svg)](https://npmjs.org/package/entities) [![Node.js CI](https://github.com/fb55/entities/actions/workflows/nodejs-test.yml/badge.svg)](https://github.com/fb55/entities/actions/workflows/nodejs-test.yml) |
| apps/vscode-extension/node_modules/environment/readme.md | no | 94 | b3deebff84858aac | # environment |
| apps/vscode-extension/node_modules/es-define-property/CHANGELOG.md | no | 29 | fe3c3c181877529c | # Changelog |
| apps/vscode-extension/node_modules/es-define-property/README.md | no | 49 | 5ce564bb53fafd87 | # es-define-property <sup>[![Version Badge][npm-version-svg]][package-url]</sup> |
| apps/vscode-extension/node_modules/es-errors/CHANGELOG.md | no | 40 | f21ce3b58b9c0018 | # Changelog |
| apps/vscode-extension/node_modules/es-errors/README.md | no | 55 | 176ec91db928c929 | # es-errors <sup>[![Version Badge][npm-version-svg]][package-url]</sup> |
| apps/vscode-extension/node_modules/es-object-atoms/CHANGELOG.md | no | 44 | a3b70f7caa0d8211 | # Changelog |
| apps/vscode-extension/node_modules/es-object-atoms/README.md | no | 63 | 7ed12f453b83efdb | # es-object-atoms <sup>[![Version Badge][npm-version-svg]][package-url]</sup> |
| apps/vscode-extension/node_modules/es-set-tostringtag/CHANGELOG.md | no | 67 | 79a874acb654eab7 | # Changelog |
| apps/vscode-extension/node_modules/es-set-tostringtag/README.md | no | 53 | d98d41a011e45ff7 | # es-set-tostringtag <sup>[![Version Badge][npm-version-svg]][package-url]</sup> |
| apps/vscode-extension/node_modules/expand-template/README.md | no | 43 | f366ba7a74be0614 | # expand-template |
| apps/vscode-extension/node_modules/fast-deep-equal/README.md | no | 96 | ada32c1b53bd7464 | # fast-deep-equal |
| apps/vscode-extension/node_modules/fast-glob/README.md | no | 830 | 79f0f5030295ab4e | # fast-glob |
| apps/vscode-extension/node_modules/fast-uri/README.md | no | 152 | 55449f95eb4b7b69 | # fast-uri |
| apps/vscode-extension/node_modules/fastq/README.md | no | 310 | e79633b399f78c1c | # fastq |
| apps/vscode-extension/node_modules/fastq/SECURITY.md | no | 15 | d0614fe0e0f9034c | # Security Policy |
| apps/vscode-extension/node_modules/fd-slicer/CHANGELOG.md | no | 49 | 1f7e7484c0cb3566 | ### 1.0.1 |
| apps/vscode-extension/node_modules/fd-slicer/README.md | no | 199 | f076c4b37c5742ab | # fd-slicer |
| apps/vscode-extension/node_modules/fill-range/README.md | no | 237 | e78ddba4ae383a98 | # fill-range [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=W8YFZ425KND68) [![NPM version](https://img.shields.io/npm/v/fill-range.svg?style=flat)](https://www.npmjs.com/package/fill-range) [![NPM monthly downloads](https://img.shields.io/npm/dm/fill-range.svg?style=flat)](https://npmjs.org/package/fill-range) [![NPM total downloads](https://img.shields.io/npm/dt/fill-range.svg?style=flat)](https://npmjs.org/package/fill-range) [![Linux Build Status](https://img.shields.io/travis/jonschlinkert/fill-range.svg?style=flat&label=Travis)](https://travis-ci.org/jonschlinkert/fill-range) |
| apps/vscode-extension/node_modules/foreground-child/README.md | no | 128 | 281516e35971919c | # foreground-child |
| apps/vscode-extension/node_modules/form-data/CHANGELOG.md | no | 686 | a9dd5ad0e5be201b | # Changelog |
| apps/vscode-extension/node_modules/form-data/README.md | no | 355 | be892a88fab4d3db | # Form-Data [![NPM Module](https://img.shields.io/npm/v/form-data.svg)](https://www.npmjs.com/package/form-data) [![Join the chat at https://gitter.im/form-data/form-data](http://form-data.github.io/images/gitterbadge.svg)](https://gitter.im/form-data/form-data) |
| apps/vscode-extension/node_modules/fs-constants/README.md | no | 26 | 389703f7ccc01444 | # fs-constants |
| apps/vscode-extension/node_modules/fs-extra/README.md | no | 293 | 62e06960c4629009 | ### CommonJS |
| apps/vscode-extension/node_modules/function-bind/.github/SECURITY.md | no | 3 | dd880fbe091e1b4f | # Security |
| apps/vscode-extension/node_modules/function-bind/CHANGELOG.md | no | 136 | c44d3c98a0cf4f95 | # Changelog |
| apps/vscode-extension/node_modules/function-bind/README.md | no | 46 | 305fc05a184a5afa | # function-bind <sup>[![Version Badge][npm-version-svg]][package-url]</sup> |
| apps/vscode-extension/node_modules/get-east-asian-width/readme.md | no | 65 | 19ad661125fa483a | # get-east-asian-width |
| apps/vscode-extension/node_modules/get-intrinsic/CHANGELOG.md | no | 186 | e73856f1e09b5743 | # Changelog |
| apps/vscode-extension/node_modules/get-intrinsic/README.md | no | 71 | 15f5365e3e1d4182 | # get-intrinsic <sup>[![Version Badge][npm-version-svg]][package-url]</sup> |
| apps/vscode-extension/node_modules/get-proto/CHANGELOG.md | no | 21 | 11759506474827be | # Changelog |
| apps/vscode-extension/node_modules/get-proto/README.md | no | 50 | 5a3c611a2e47ccbe | # get-proto <sup>[![Version Badge][npm-version-svg]][package-url]</sup> |
| apps/vscode-extension/node_modules/glob-parent/CHANGELOG.md | no | 110 | 3a7de772276d39da | ### [5.1.2](https://github.com/gulpjs/glob-parent/compare/v5.1.1...v5.1.2) (2021-03-06) |
| apps/vscode-extension/node_modules/glob-parent/README.md | no | 137 | 3fdaad1cc34c596c | # glob-parent |
| apps/vscode-extension/node_modules/glob/LICENSE.md | no | 63 | a49c9ba464796f65 | # Blue Oak Model License |
| apps/vscode-extension/node_modules/glob/node_modules/balanced-match/LICENSE.md | no | 23 | d408f38ffa3355c5 | (no markdown heading) |
| apps/vscode-extension/node_modules/glob/node_modules/balanced-match/README.md | no | 57 | 68b91fa8a0b15466 | # balanced-match |
| apps/vscode-extension/node_modules/glob/node_modules/brace-expansion/README.md | no | 105 | e93dbbc034d09eb6 | # brace-expansion |
| apps/vscode-extension/node_modules/glob/node_modules/minimatch/LICENSE.md | no | 55 | 2c7c5d22ed5a8ee9 | # Blue Oak Model License |
| apps/vscode-extension/node_modules/glob/node_modules/minimatch/README.md | no | 528 | d0e7683a7fcabec7 | # minimatch |
| apps/vscode-extension/node_modules/glob/README.md | no | 1294 | 09d53d6dd61ecd53 | # Glob |
| apps/vscode-extension/node_modules/globby/readme.md | no | 210 | 2471760693376784 | # globby |
| apps/vscode-extension/node_modules/gopd/CHANGELOG.md | no | 45 | aba458bfc8c4bdc9 | # Changelog |
| apps/vscode-extension/node_modules/gopd/README.md | no | 40 | a5adda11eb1b5c4a | # gopd <sup>[![Version Badge][npm-version-svg]][package-url]</sup> |
| apps/vscode-extension/node_modules/graceful-fs/README.md | no | 143 | 1c8169c6bd7d7c96 | # graceful-fs |
| apps/vscode-extension/node_modules/has-flag/readme.md | no | 89 | e9f8f4e5c1e63047 | # has-flag [![Build Status](https://travis-ci.org/sindresorhus/has-flag.svg?branch=master)](https://travis-ci.org/sindresorhus/has-flag) |
| apps/vscode-extension/node_modules/has-symbols/CHANGELOG.md | no | 91 | ad7ead4963a1958e | # Changelog |
| apps/vscode-extension/node_modules/has-symbols/README.md | no | 46 | a062b27ee12e84e3 | # has-symbols <sup>[![Version Badge][2]][1]</sup> |
| apps/vscode-extension/node_modules/has-tostringtag/CHANGELOG.md | no | 42 | 6c721d97055e8381 | # Changelog |
| apps/vscode-extension/node_modules/has-tostringtag/README.md | no | 46 | bcf8eec2c348d450 | # has-tostringtag <sup>[![Version Badge][2]][1]</sup> |
| apps/vscode-extension/node_modules/hasown/CHANGELOG.md | no | 58 | dbb1b9d059ec30fa | # Changelog |
| apps/vscode-extension/node_modules/hasown/README.md | no | 40 | a922ab2a0abcdcbd | # hasown <sup>[![Version Badge][npm-version-svg]][package-url]</sup> |
| apps/vscode-extension/node_modules/hosted-git-info/README.md | no | 133 | 0f8f42eff0ccc33a | # hosted-git-info |
| apps/vscode-extension/node_modules/htmlparser2/node_modules/entities/readme.md | no | 143 | 4c41aeb394d33187 | # entities [![NPM version](https://img.shields.io/npm/v/entities.svg)](https://npmjs.org/package/entities) [![Downloads](https://img.shields.io/npm/dm/entities.svg)](https://npmjs.org/package/entities) [![Node.js CI](https://github.com/fb55/entities/actions/workflows/nodejs-test.yml/badge.svg)](https://github.com/fb55/entities/actions/workflows/nodejs-test.yml) |
| apps/vscode-extension/node_modules/htmlparser2/README.md | no | 171 | c97a824f6828a5ab | # htmlparser2 |
| apps/vscode-extension/node_modules/http-proxy-agent/README.md | no | 44 | c34be87fe9b9da00 | ### An HTTP(s) proxy `http.Agent` implementation for HTTP |
| apps/vscode-extension/node_modules/https-proxy-agent/README.md | no | 70 | 462697a398c1bbbf | ### An HTTP(s) proxy `http.Agent` implementation for HTTPS |
| apps/vscode-extension/node_modules/iconv-lite/Changelog.md | no | 212 | c9826c350eefe700 | ## 0.6.3 / 2021-05-23 |
| apps/vscode-extension/node_modules/iconv-lite/README.md | no | 130 | d320d84b29280ae7 | ## iconv-lite: Pure JS character encoding conversion |
| apps/vscode-extension/node_modules/ieee754/README.md | no | 51 | 27827383727dcc6b | # ieee754 [![travis][travis-image]][travis-url] [![npm][npm-image]][npm-url] [![downloads][downloads-image]][downloads-url] [![javascript style guide][standard-image]][standard-url] |
| apps/vscode-extension/node_modules/ignore/README.md | no | 501 | edc4cc02c75bd432 | # ignore |
| apps/vscode-extension/node_modules/immediate/README.md | no | 93 | f8ba840a9e01f16c | # immediate [![Build Status](https://travis-ci.org/calvinmetcalf/immediate.svg?branch=master)](https://travis-ci.org/calvinmetcalf/immediate) |
| apps/vscode-extension/node_modules/index-to-position/readme.md | no | 59 | 8eb87d3374b051d6 | # index-to-position |
| apps/vscode-extension/node_modules/inherits/README.md | no | 42 | b33c8be1ca837d9e | ## usage |
| apps/vscode-extension/node_modules/ini/README.md | no | 102 | 128be3868807fd5a | ## Usage |
| apps/vscode-extension/node_modules/is-docker/readme.md | no | 27 | 5ee94a7a38d157a5 | # is-docker |
| apps/vscode-extension/node_modules/is-extglob/README.md | no | 107 | bb36a84b32da3f9c | # is-extglob [![NPM version](https://img.shields.io/npm/v/is-extglob.svg?style=flat)](https://www.npmjs.com/package/is-extglob) [![NPM downloads](https://img.shields.io/npm/dm/is-extglob.svg?style=flat)](https://npmjs.org/package/is-extglob) [![Build Status](https://img.shields.io/travis/jonschlinkert/is-extglob.svg?style=flat)](https://travis-ci.org/jonschlinkert/is-extglob) |
| apps/vscode-extension/node_modules/is-fullwidth-code-point/readme.md | no | 39 | 17df4cd59773b379 | # is-fullwidth-code-point [![Build Status](https://travis-ci.org/sindresorhus/is-fullwidth-code-point.svg?branch=master)](https://travis-ci.org/sindresorhus/is-fullwidth-code-point) |
| apps/vscode-extension/node_modules/is-glob/README.md | no | 206 | e42512412a98a913 | # is-glob [![NPM version](https://img.shields.io/npm/v/is-glob.svg?style=flat)](https://www.npmjs.com/package/is-glob) [![NPM monthly downloads](https://img.shields.io/npm/dm/is-glob.svg?style=flat)](https://npmjs.org/package/is-glob) [![NPM total downloads](https://img.shields.io/npm/dt/is-glob.svg?style=flat)](https://npmjs.org/package/is-glob) [![Build Status](https://img.shields.io/github/workflow/status/micromatch/is-glob/dev)](https://github.com/micromatch/is-glob/actions) |
| apps/vscode-extension/node_modules/is-inside-container/readme.md | no | 36 | 4d081dd53cde37a4 | # is-inside-container |
| apps/vscode-extension/node_modules/is-interactive/readme.md | no | 52 | 2c982bc90862fb84 | # is-interactive |
| apps/vscode-extension/node_modules/is-number/README.md | no | 187 | 8e676a0587ba3508 | # is-number [![NPM version](https://img.shields.io/npm/v/is-number.svg?style=flat)](https://www.npmjs.com/package/is-number) [![NPM monthly downloads](https://img.shields.io/npm/dm/is-number.svg?style=flat)](https://npmjs.org/package/is-number) [![NPM total downloads](https://img.shields.io/npm/dt/is-number.svg?style=flat)](https://npmjs.org/package/is-number) [![Linux Build Status](https://img.shields.io/travis/jonschlinkert/is-number.svg?style=flat&label=Travis)](https://travis-ci.org/jonschlinkert/is-number) |
| apps/vscode-extension/node_modules/is-unicode-supported/readme.md | no | 35 | 44da295b517a9553 | # is-unicode-supported |
| apps/vscode-extension/node_modules/is-wsl/readme.md | no | 21 | e9e24c9f5d27ec60 | # is-wsl |
| apps/vscode-extension/node_modules/isarray/README.md | no | 60 | ff138e683771b187 | # isarray |
| apps/vscode-extension/node_modules/isexe/README.md | no | 51 | ab12ff031a831156 | # isexe |
| apps/vscode-extension/node_modules/istextorbinary/LICENSE.md | no | 101 | 5fdbfb4ce1eb9581 | # License |
| apps/vscode-extension/node_modules/istextorbinary/README.md | no | 229 | 796323fb4e6881e2 | # Is Text or Binary? |
| apps/vscode-extension/node_modules/istextorbinary/SECURITY.md | no | 21 | c09ebbdd2b4a742d | # Security Policy |
| apps/vscode-extension/node_modules/jackspeak/LICENSE.md | no | 55 | 2c7c5d22ed5a8ee9 | # Blue Oak Model License |
| apps/vscode-extension/node_modules/jackspeak/README.md | no | 394 | 2efbdaf591013643 | # jackspeak |
| apps/vscode-extension/node_modules/js-tokens/CHANGELOG.md | no | 151 | 79291b8c48329385 | ### Version 4.0.0 (2018-01-28) ### |
| apps/vscode-extension/node_modules/js-tokens/README.md | no | 240 | 21ef7d86f3372ba0 | ### `jsTokens` ### |
| apps/vscode-extension/node_modules/js-yaml/README.md | no | 233 | aa65504ff91c42c9 | ### YAML module for node.js |
| apps/vscode-extension/node_modules/json-schema-traverse/README.md | no | 95 | e6137660d373bc51 | # json-schema-traverse |
| apps/vscode-extension/node_modules/json5/LICENSE.md | no | 23 | 53e59feb13058722 | (no markdown heading) |
| apps/vscode-extension/node_modules/json5/README.md | no | 282 | 93c950af1dea94ec | # JSON5 – JSON for Humans |
| apps/vscode-extension/node_modules/jsonc-parser/CHANGELOG.md | no | 76 | e8e1c80842a20b52 | (no markdown heading) |
| apps/vscode-extension/node_modules/jsonc-parser/LICENSE.md | no | 21 | c3a24c02d678e5f0 | (no markdown heading) |
| apps/vscode-extension/node_modules/jsonc-parser/README.md | no | 364 | dbd5441ae6226fb8 | # jsonc-parser |
| apps/vscode-extension/node_modules/jsonc-parser/SECURITY.md | no | 41 | 830e94b83c3b6f45 | ## Security |
| apps/vscode-extension/node_modules/jsonfile/README.md | no | 230 | 9c91f7c277625413 | ### readFile(filename, [options], callback) |
| apps/vscode-extension/node_modules/jsonwebtoken/README.md | no | 396 | e57a769be325a07c | # jsonwebtoken |
| apps/vscode-extension/node_modules/jszip/CHANGES.md | no | 210 | 7e07acb69b5b0f2b | ### v3.10.2 2026-09-09 |
| apps/vscode-extension/node_modules/jszip/node_modules/readable-stream/CONTRIBUTING.md | no | 38 | 56e4e12a6934a2c4 | # Developer's Certificate of Origin 1.1 |
| apps/vscode-extension/node_modules/jszip/node_modules/readable-stream/doc/wg-meetings/2015-01-30.md | no | 60 | 39bdf2c2d8d23df3 | # streams WG Meeting 2015-01-30 |
| apps/vscode-extension/node_modules/jszip/node_modules/readable-stream/GOVERNANCE.md | no | 136 | 7a521e462d1c6f3b | ### Streams Working Group |
| apps/vscode-extension/node_modules/jszip/node_modules/readable-stream/README.md | no | 58 | 5a917d93a11215fb | # readable-stream |
| apps/vscode-extension/node_modules/jszip/node_modules/safe-buffer/README.md | no | 584 | d301a85080877571 | # safe-buffer [![travis][travis-image]][travis-url] [![npm][npm-image]][npm-url] [![downloads][downloads-image]][downloads-url] [![javascript style guide][standard-image]][standard-url] |
| apps/vscode-extension/node_modules/jszip/node_modules/string_decoder/README.md | no | 47 | 64417fec74bed1e4 | # string_decoder |
| apps/vscode-extension/node_modules/jszip/sponsors.md | no | 21 | 05023a2cdb8fbddf | ## 💎 Diamond |
| apps/vscode-extension/node_modules/jwa/README.md | no | 150 | 2273f282b7e98c67 | # node-jwa [![Build Status](https://travis-ci.org/brianloveswords/node-jwa.svg?branch=master)](https://travis-ci.org/brianloveswords/node-jwa) |
| apps/vscode-extension/node_modules/jws/CHANGELOG.md | no | 56 | aa214975b1426ce4 | # Change Log |
| apps/vscode-extension/node_modules/jws/readme.md | no | 255 | 19ede149863e882b | # node-jws [![Build Status](https://secure.travis-ci.org/brianloveswords/node-jws.svg)](http://travis-ci.org/brianloveswords/node-jws) |
| apps/vscode-extension/node_modules/keytar/LICENSE.md | no | 20 | 224fcc506ef97afd | (no markdown heading) |
| apps/vscode-extension/node_modules/keytar/README.md | no | 94 | 78ad6be6f43aad31 | # keytar - Node module to manage system keychain |
| apps/vscode-extension/node_modules/leven/readme.md | no | 50 | 4fa85d2dee529dd0 | # leven [![Build Status](https://travis-ci.org/sindresorhus/leven.svg?branch=master)](https://travis-ci.org/sindresorhus/leven) |
| apps/vscode-extension/node_modules/lie/license.md | no | 7 | 5c81b0caa9859340 | #Copyright (c) 2014-2018 Calvin Metcalf, Jordan Harband |
| apps/vscode-extension/node_modules/lie/README.md | no | 62 | 97a1e33c510ea9ce | # lie |
| apps/vscode-extension/node_modules/linkify-it/README.md | no | 195 | cd64a088d7a900eb | ##### Example 1 |
| apps/vscode-extension/node_modules/lodash.includes/README.md | no | 18 | baea08cbf4d642e0 | # lodash.includes v4.3.0 |
| apps/vscode-extension/node_modules/lodash.isboolean/README.md | no | 18 | e7c286f0810d2b89 | # lodash.isboolean v3.0.3 |
| apps/vscode-extension/node_modules/lodash.isinteger/README.md | no | 18 | d97158b83bf82cbb | # lodash.isinteger v4.0.4 |
| apps/vscode-extension/node_modules/lodash.isnumber/README.md | no | 18 | 14e23253247dad45 | # lodash.isnumber v3.0.3 |
| apps/vscode-extension/node_modules/lodash.isplainobject/README.md | no | 18 | e16673134b617aea | # lodash.isplainobject v4.0.6 |
| apps/vscode-extension/node_modules/lodash.isstring/README.md | no | 18 | 9df20abc572c6aa3 | # lodash.isstring v4.0.1 |
| apps/vscode-extension/node_modules/lodash.once/README.md | no | 18 | 15996ffb63cf9a1b | # lodash.once v4.1.1 |
| apps/vscode-extension/node_modules/lodash.truncate/README.md | no | 18 | c7e934b790abad08 | # lodash.truncate v4.4.2 |
| apps/vscode-extension/node_modules/lodash/README.md | no | 39 | 159abc800864ddc9 | # lodash v4.18.1 |
| apps/vscode-extension/node_modules/log-symbols/node_modules/chalk/readme.md | no | 297 | 03d260b86ecf3bec | ## Info |
| apps/vscode-extension/node_modules/log-symbols/node_modules/is-unicode-supported/readme.md | no | 35 | 44da295b517a9553 | # is-unicode-supported |
| apps/vscode-extension/node_modules/log-symbols/readme.md | no | 39 | 6917f5026ee2a3d9 | # log-symbols |
| apps/vscode-extension/node_modules/lru-cache/README.md | no | 166 | 981a9b1f5cffb2d7 | # lru cache |
| apps/vscode-extension/node_modules/markdown-it/README.md | no | 320 | b8476703fabd0543 | # markdown-it <!-- omit in toc --> |
| apps/vscode-extension/node_modules/math-intrinsics/CHANGELOG.md | no | 24 | 1868f81797e7249a | # Changelog |
| apps/vscode-extension/node_modules/math-intrinsics/README.md | no | 50 | 9ac2e749aed9f825 | # math-intrinsics <sup>[![Version Badge][npm-version-svg]][package-url]</sup> |
| apps/vscode-extension/node_modules/mdurl/README.md | no | 102 | 4cf58538aeba8f55 | # mdurl |
| apps/vscode-extension/node_modules/merge2/README.md | no | 144 | 57edba613c3742bd | # merge2 |
| apps/vscode-extension/node_modules/micromatch/README.md | no | 1024 | d687a4b9ff64755f | # micromatch [![NPM version](https://img.shields.io/npm/v/micromatch.svg?style=flat)](https://www.npmjs.com/package/micromatch) [![NPM monthly downloads](https://img.shields.io/npm/dm/micromatch.svg?style=flat)](https://npmjs.org/package/micromatch) [![NPM total downloads](https://img.shields.io/npm/dt/micromatch.svg?style=flat)](https://npmjs.org/package/micromatch)  [![Tests](https://github.com/micromatch/micromatch/actions/workflows/test.yml/badge.svg)](https://github.com/micromatch/micromatch/actions/workflows/test.yml) |
| apps/vscode-extension/node_modules/mime-db/HISTORY.md | no | 507 | 1e820a4ab3b25cc8 | (no markdown heading) |
| apps/vscode-extension/node_modules/mime-db/README.md | no | 100 | 5cc863fd64953afa | # mime-db |
| apps/vscode-extension/node_modules/mime-types/HISTORY.md | no | 397 | 277b1cfc3e8fdb57 | (no markdown heading) |
| apps/vscode-extension/node_modules/mime-types/README.md | no | 113 | 19e8eaca7dc91f7a | # mime-types |
| apps/vscode-extension/node_modules/mime/CHANGELOG.md | no | 164 | cb69ab3f4934b697 | # Changelog |
| apps/vscode-extension/node_modules/mime/README.md | no | 90 | 3d645cf326552be6 | # mime |
| apps/vscode-extension/node_modules/mimic-function/readme.md | no | 80 | a8a76b02b6d414cb | ## Install |
| apps/vscode-extension/node_modules/mimic-response/readme.md | no | 78 | 777c0925baf28376 | # mimic-response [![Build Status](https://travis-ci.com/sindresorhus/mimic-response.svg?branch=master)](https://travis-ci.com/sindresorhus/mimic-response) |
| apps/vscode-extension/node_modules/minimatch/README.md | no | 267 | 2c77413d09683837 | # minimatch |
| apps/vscode-extension/node_modules/minimist/CHANGELOG.md | no | 298 | f6c131dccabc16cc | # Changelog |
| apps/vscode-extension/node_modules/minimist/README.md | no | 121 | a56e078a4586bb86 | # minimist <sup>[![Version Badge][npm-version-svg]][package-url]</sup> |
| apps/vscode-extension/node_modules/minipass/LICENSE.md | no | 55 | 8a1af140fdfbf5af | # Blue Oak Model License |
| apps/vscode-extension/node_modules/minipass/README.md | no | 825 | 69b9d3a872f51d63 | # minipass |
| apps/vscode-extension/node_modules/mkdirp-classic/README.md | no | 18 | 944ac66177fb5184 | # mkdirp-classic |
| apps/vscode-extension/node_modules/ms/license.md | no | 21 | 1662fae9b5314d11 | (no markdown heading) |
| apps/vscode-extension/node_modules/ms/readme.md | no | 59 | 8bf6c4f414b123ea | # ms |
| apps/vscode-extension/node_modules/mute-stream/README.md | no | 68 | e52d595c64550a4d | # mute-stream |
| apps/vscode-extension/node_modules/napi-build-utils/index.md | no | 0 | e3b0c44298fc1c14 | (no markdown heading) |
| apps/vscode-extension/node_modules/napi-build-utils/README.md | no | 52 | 8a372a57ba70da07 | # napi-build-utils |
| apps/vscode-extension/node_modules/node-abi/README.md | no | 54 | 2b7a9c42b4b3fb80 | # Node.js ABI |
| apps/vscode-extension/node_modules/node-addon-api/LICENSE.md | no | 13 | 4fcf69bbecb999ec | (no markdown heading) |
| apps/vscode-extension/node_modules/node-addon-api/README.md | no | 293 | 13be3e52775410f5 | # **node-addon-api module** |
| apps/vscode-extension/node_modules/node-addon-api/tools/README.md | no | 73 | 65e9ea918538f453 | # Tools |
| apps/vscode-extension/node_modules/node-sarif-builder/CHANGELOG.md | no | 66 | 3abdec83f7659018 | # Changelog |
| apps/vscode-extension/node_modules/node-sarif-builder/README.md | no | 222 | 99a163bff477bc68 | # node-sarif-builder |
| apps/vscode-extension/node_modules/normalize-package-data/node_modules/hosted-git-info/README.md | no | 133 | e744b0c855d114e5 | # hosted-git-info |
| apps/vscode-extension/node_modules/normalize-package-data/node_modules/lru-cache/README.md | no | 331 | 95e8c2a08632fe00 | # lru-cache |
| apps/vscode-extension/node_modules/normalize-package-data/README.md | no | 108 | 1e7b1258552c912c | # normalize-package-data |
| apps/vscode-extension/node_modules/nth-check/README.md | no | 136 | 486e46fcb359a74f | # nth-check [![Build Status](https://travis-ci.org/fb55/nth-check.svg)](https://travis-ci.org/fb55/nth-check) |
| apps/vscode-extension/node_modules/object-inspect/CHANGELOG.md | no | 424 | 2a4cce1ade3b0d29 | # Changelog |
| apps/vscode-extension/node_modules/once/README.md | no | 79 | 43b6d72bb23aff98 | # once |
| apps/vscode-extension/node_modules/onetime/readme.md | no | 88 | 672e94175fe37dbc | # onetime |
| apps/vscode-extension/node_modules/open/readme.md | no | 183 | ef7c73b2c244bd63 | # open |
| apps/vscode-extension/node_modules/ora/node_modules/chalk/readme.md | no | 297 | 03d260b86ecf3bec | ## Info |
| apps/vscode-extension/node_modules/ora/node_modules/emoji-regex/README.md | no | 107 | f8ca51b375b32e0a | # emoji-regex [![Build status](https://github.com/mathiasbynens/emoji-regex/actions/workflows/main.yml/badge.svg)](https://github.com/mathiasbynens/emoji-regex/actions/workflows/main.yml) [![emoji-regex on npm](https://img.shields.io/npm/v/emoji-regex)](https://www.npmjs.com/package/emoji-regex) |
| apps/vscode-extension/node_modules/ora/node_modules/string-width/readme.md | no | 66 | 9aeeb742159fcc51 | # string-width |
| apps/vscode-extension/node_modules/ora/readme.md | no | 329 | f426167a142d9bdf | # ora |
| apps/vscode-extension/node_modules/p-map/readme.md | no | 190 | df3cabe97595f646 | # p-map |
| apps/vscode-extension/node_modules/package-json-from-dist/LICENSE.md | no | 63 | a49c9ba464796f65 | # Blue Oak Model License |
| apps/vscode-extension/node_modules/package-json-from-dist/README.md | no | 110 | 4c5daff6bf243549 | # package-json-from-dist |
| apps/vscode-extension/node_modules/pako/CHANGELOG.md | no | 164 | 8d3b2a5ff30f052a | # Changelog |
| apps/vscode-extension/node_modules/pako/README.md | no | 191 | 8174ca473d9df9da | (no markdown heading) |
| apps/vscode-extension/node_modules/parse-json/readme.md | no | 119 | a9cb9bfc05d044df | # parse-json |
| apps/vscode-extension/node_modules/parse-semver/CHANGELOG.md | no | 27 | 1a8772f616015e36 | ## 1.1.1 / 2016-02-23 |
| apps/vscode-extension/node_modules/parse-semver/CONTRIBUTING.md | no | 32 | 5eaed0772c0f8bf8 | # Contributing Guidelines |
| apps/vscode-extension/node_modules/parse-semver/LICENSE.md | no | 21 | 3434744a98fe97a8 | # The MIT License |
| apps/vscode-extension/node_modules/parse-semver/node_modules/semver/README.md | no | 412 | fb882cec291aada2 | ## Install |
| apps/vscode-extension/node_modules/parse-semver/README.md | no | 104 | 3be39abf028335f6 | # [parse-semver][author-www-url] [![npmjs.com][npmjs-img]][npmjs-url] [![The MIT License][license-img]][license-url] |
| apps/vscode-extension/node_modules/parse5-htmlparser2-tree-adapter/README.md | no | 34 | 7d6191fe38547ddf | (no markdown heading) |
| apps/vscode-extension/node_modules/parse5-parser-stream/README.md | no | 34 | 5120f9c372dfe9b8 | (no markdown heading) |
| apps/vscode-extension/node_modules/parse5/node_modules/entities/readme.md | no | 122 | cb67cf2e1ff9c1f9 | # entities [![NPM version](https://img.shields.io/npm/v/entities.svg)](https://npmjs.org/package/entities) [![Downloads](https://img.shields.io/npm/dm/entities.svg)](https://npmjs.org/package/entities) [![Node.js CI](https://github.com/fb55/entities/actions/workflows/nodejs-test.yml/badge.svg)](https://github.com/fb55/entities/actions/workflows/nodejs-test.yml) |
| apps/vscode-extension/node_modules/parse5/README.md | no | 38 | ba4e9702964c97d1 | (no markdown heading) |
| apps/vscode-extension/node_modules/path-key/readme.md | no | 61 | dcd0d891bc1a13ee | # path-key [![Build Status](https://travis-ci.org/sindresorhus/path-key.svg?branch=master)](https://travis-ci.org/sindresorhus/path-key) |
| apps/vscode-extension/node_modules/path-scurry/LICENSE.md | no | 55 | 8a1af140fdfbf5af | # Blue Oak Model License |
| apps/vscode-extension/node_modules/path-scurry/node_modules/lru-cache/LICENSE.md | no | 55 | 8a1af140fdfbf5af | # Blue Oak Model License |
| apps/vscode-extension/node_modules/path-scurry/node_modules/lru-cache/README.md | no | 469 | 9ce0167d06ee43ab | # lru-cache |
| apps/vscode-extension/node_modules/path-scurry/README.md | no | 636 | 13bde511569d6d63 | # path-scurry |
| apps/vscode-extension/node_modules/path-type/readme.md | no | 62 | d242135845d5f04f | # path-type |
| apps/vscode-extension/node_modules/pend/README.md | no | 41 | 4039da3645c08232 | # Pend |
| apps/vscode-extension/node_modules/picocolors/README.md | no | 21 | 5027b2836551ea0f | # picocolors |
| apps/vscode-extension/node_modules/picomatch/README.md | no | 716 | f4653b68a1883a32 | ## Why picomatch? |
| apps/vscode-extension/node_modules/pluralize/Readme.md | no | 100 | e0f59c6c4d49858c | # Pluralize |
| apps/vscode-extension/node_modules/prebuild-install/CHANGELOG.md | no | 131 | 7e4c2d7091ded670 | # Changelog |
| apps/vscode-extension/node_modules/prebuild-install/CONTRIBUTING.md | no | 6 | e65a6c8971149d9c | # Contributing to prebuild |
| apps/vscode-extension/node_modules/prebuild-install/README.md | no | 163 | 56e2065c004fadd2 | # prebuild-install |
| apps/vscode-extension/node_modules/process-nextick-args/license.md | no | 19 | ecdccbcf39024f62 | # Copyright (c) 2015 Calvin Metcalf |
| apps/vscode-extension/node_modules/process-nextick-args/readme.md | no | 18 | f659caaae9d9f4a8 | (no markdown heading) |
| apps/vscode-extension/node_modules/pump/README.md | no | 74 | 917d565b1c10dad5 | # pump |
| apps/vscode-extension/node_modules/pump/SECURITY.md | no | 5 | 994ea9cf579d2164 | ## Security contact information |
| apps/vscode-extension/node_modules/punycode.js/README.md | no | 148 | ab87f92cff7bfac2 | # Punycode.js [![punycode on npm](https://img.shields.io/npm/v/punycode)](https://www.npmjs.com/package/punycode) [![](https://data.jsdelivr.com/v1/package/npm/punycode/badge)](https://www.jsdelivr.com/package/npm/punycode) |
| apps/vscode-extension/node_modules/qs/.github/SECURITY.md | no | 11 | 51e490f9a23ac20c | # Security |
| apps/vscode-extension/node_modules/qs/.github/THREAT_MODEL.md | no | 78 | 6a666b5d4079260b | ## Threat Model for qs (querystring parsing library) |
| apps/vscode-extension/node_modules/qs/CHANGELOG.md | no | 848 | 64175dd893c83c3d | ## **6.16.0** |
| apps/vscode-extension/node_modules/qs/LICENSE.md | no | 29 | e7dc37bf662d7f78 | (no markdown heading) |
| apps/vscode-extension/node_modules/qs/README.md | no | 776 | 05659085ecff6080 | # qs <sup>[![Version Badge][npm-version-svg]][package-url]</sup> |
| apps/vscode-extension/node_modules/queue-microtask/README.md | no | 90 | 3a8d322db8edf9a4 | # queue-microtask [![ci][ci-image]][ci-url] [![npm][npm-image]][npm-url] [![downloads][downloads-image]][downloads-url] [![javascript style guide][standard-image]][standard-url] |
| apps/vscode-extension/node_modules/rc-config-loader/README.md | no | 223 | b84dc00e2485df40 | # rc-config-loader [![Actions Status: test](https://github.com/azu/rc-config-loader/workflows/test/badge.svg)](https://github.com/azu/rc-config-loader/actions?query=workflow%3A"test") |
| apps/vscode-extension/node_modules/rc/README.md | no | 227 | 3088babbed9971cd | # rc |
| apps/vscode-extension/node_modules/read-pkg/node_modules/unicorn-magic/readme.md | no | 25 | 968ca1b138df60e1 | # unicorn-magic |
| apps/vscode-extension/node_modules/read-pkg/readme.md | no | 81 | a624e8254bf1ebf2 | # read-pkg |
| apps/vscode-extension/node_modules/read/README.md | no | 53 | 567cecf376503501 | ## read |
| apps/vscode-extension/node_modules/readable-stream/CONTRIBUTING.md | no | 38 | 56e4e12a6934a2c4 | # Developer's Certificate of Origin 1.1 |
| apps/vscode-extension/node_modules/readable-stream/GOVERNANCE.md | no | 136 | 7a521e462d1c6f3b | ### Streams Working Group |
| apps/vscode-extension/node_modules/readable-stream/README.md | no | 106 | 93e374225fa62e8b | # readable-stream |
| apps/vscode-extension/node_modules/require-from-string/readme.md | no | 56 | 969286b710026d91 | # require-from-string [![Build Status](https://travis-ci.org/floatdrop/require-from-string.svg?branch=master)](https://travis-ci.org/floatdrop/require-from-string) |
| apps/vscode-extension/node_modules/restore-cursor/readme.md | no | 21 | 18d977af836b648b | # restore-cursor |
| apps/vscode-extension/node_modules/reusify/README.md | no | 139 | 9df9fd0cfd741abe | # reusify |
| apps/vscode-extension/node_modules/reusify/SECURITY.md | no | 15 | d0614fe0e0f9034c | # Security Policy |
| apps/vscode-extension/node_modules/run-applescript/readme.md | no | 78 | 3cf54b7dd4d2ca6d | # run-applescript |
| apps/vscode-extension/node_modules/run-parallel/README.md | no | 85 | bca81459fb9b4392 | # run-parallel [![travis][travis-image]][travis-url] [![npm][npm-image]][npm-url] [![downloads][downloads-image]][downloads-url] [![javascript style guide][standard-image]][standard-url] |
| apps/vscode-extension/node_modules/safe-buffer/README.md | no | 584 | d301a85080877571 | # safe-buffer [![travis][travis-image]][travis-url] [![npm][npm-image]][npm-url] [![downloads][downloads-image]][downloads-url] [![javascript style guide][standard-image]][standard-url] |
| apps/vscode-extension/node_modules/safer-buffer/Porting-Buffer.md | no | 268 | 134523d05b39e177 | # Porting to the Buffer.from/Buffer.alloc API |
| apps/vscode-extension/node_modules/safer-buffer/Readme.md | no | 156 | d4331b7c5af9c021 | # safer-buffer [![travis][travis-image]][travis-url] [![npm][npm-image]][npm-url] [![javascript style guide][standard-image]][standard-url] [![Security Responsible Disclosure][secuirty-image]][secuirty-url] |
| apps/vscode-extension/node_modules/sax/LICENSE.md | no | 55 | 8a1af140fdfbf5af | # Blue Oak Model License |
| apps/vscode-extension/node_modules/sax/README.md | no | 227 | 9e6bd0717598300f | # sax js |
| apps/vscode-extension/node_modules/secretlint/README.md | no | 88 | 129b73c4aa367a0b | # secretlint |
| apps/vscode-extension/node_modules/semver/README.md | no | 680 | f1a789dcec285150 | ## Install |
| apps/vscode-extension/node_modules/shebang-command/readme.md | no | 34 | 7918385f0c22cac3 | # shebang-command [![Build Status](https://travis-ci.org/kevva/shebang-command.svg?branch=master)](https://travis-ci.org/kevva/shebang-command) |
| apps/vscode-extension/node_modules/shebang-regex/readme.md | no | 33 | e2a766922c935927 | # shebang-regex [![Build Status](https://travis-ci.org/sindresorhus/shebang-regex.svg?branch=master)](https://travis-ci.org/sindresorhus/shebang-regex) |
| apps/vscode-extension/node_modules/side-channel-list/CHANGELOG.md | no | 36 | f40ac5347b6b43c5 | # Changelog |
| apps/vscode-extension/node_modules/side-channel-list/README.md | no | 62 | 3627a589d762bb9d | # side-channel-list <sup>[![Version Badge][npm-version-svg]][package-url]</sup> |
| apps/vscode-extension/node_modules/side-channel-map/CHANGELOG.md | no | 22 | a622f46bc8b5c72a | # Changelog |
| apps/vscode-extension/node_modules/side-channel-map/README.md | no | 62 | f5a7086db928685f | # side-channel-map <sup>[![Version Badge][npm-version-svg]][package-url]</sup> |
| apps/vscode-extension/node_modules/side-channel-weakmap/CHANGELOG.md | no | 28 | c8fe52550510be7e | # Changelog |
| apps/vscode-extension/node_modules/side-channel-weakmap/README.md | no | 62 | 5c111085145d73c9 | # side-channel-weakmap <sup>[![Version Badge][npm-version-svg]][package-url]</sup> |
| apps/vscode-extension/node_modules/side-channel/CHANGELOG.md | no | 120 | f0de2c3154a59af9 | # Changelog |
| apps/vscode-extension/node_modules/side-channel/README.md | no | 61 | 2878dd11d6591880 | # side-channel <sup>[![Version Badge][npm-version-svg]][package-url]</sup> |
| apps/vscode-extension/node_modules/signal-exit/README.md | no | 74 | 253e9122e9e5eaf8 | # signal-exit |
| apps/vscode-extension/node_modules/simple-concat/README.md | no | 44 | d7d98a8abc0be19d | # simple-concat [![travis][travis-image]][travis-url] [![npm][npm-image]][npm-url] [![downloads][downloads-image]][downloads-url] [![javascript style guide][standard-image]][standard-url] |
| apps/vscode-extension/node_modules/simple-get/README.md | no | 333 | 2659d199c76750c6 | # simple-get [![ci][ci-image]][ci-url] [![npm][npm-image]][npm-url] [![downloads][downloads-image]][downloads-url] [![javascript style guide][standard-image]][standard-url] |
| apps/vscode-extension/node_modules/slash/readme.md | no | 36 | 655d109bf0dc1708 | # slash |
| apps/vscode-extension/node_modules/slice-ansi/readme.md | no | 66 | cf2f37838ed7851c | # slice-ansi [![Build Status](https://travis-ci.org/chalk/slice-ansi.svg?branch=master)](https://travis-ci.org/chalk/slice-ansi) [![XO: Linted](https://img.shields.io/badge/xo-linted-blue.svg)](https://github.com/xojs/xo) |
| apps/vscode-extension/node_modules/spdx-correct/README.md | no | 22 | 0f394fce232beca4 | ## Usage |
| apps/vscode-extension/node_modules/spdx-exceptions/README.md | no | 36 | 554b19eee11d2964 | ## Copyright and Licensing |
| apps/vscode-extension/node_modules/spdx-expression-parse/README.md | no | 91 | db8a2293bf9d1b90 | (no markdown heading) |
| apps/vscode-extension/node_modules/spdx-license-ids/README.md | no | 51 | b4807793db6058c8 | # spdx-license-ids |
| apps/vscode-extension/node_modules/stdin-discarder/readme.md | no | 37 | 87f45bafd739d6be | # stdin-discarder |
| apps/vscode-extension/node_modules/string-width/node_modules/ansi-regex/readme.md | no | 78 | 3ebc0f845b1bab50 | # ansi-regex |
| apps/vscode-extension/node_modules/string-width/node_modules/strip-ansi/readme.md | no | 46 | cb384db30337ecec | # strip-ansi [![Build Status](https://travis-ci.org/chalk/strip-ansi.svg?branch=master)](https://travis-ci.org/chalk/strip-ansi) |
| apps/vscode-extension/node_modules/string-width/readme.md | no | 50 | cd4aaf53cc7df421 | # string-width |
| apps/vscode-extension/node_modules/string_decoder/README.md | no | 47 | 64417fec74bed1e4 | # string_decoder |
| apps/vscode-extension/node_modules/strip-ansi/readme.md | no | 37 | 97c8f78e30d8dd4f | # strip-ansi |
| apps/vscode-extension/node_modules/strip-json-comments/readme.md | no | 64 | 94092712ac3a2619 | # strip-json-comments [![Build Status](https://travis-ci.org/sindresorhus/strip-json-comments.svg?branch=master)](https://travis-ci.org/sindresorhus/strip-json-comments) |
| apps/vscode-extension/node_modules/structured-source/README.md | no | 70 | 85ac3fd7eef0f7df | # StructuredSource [![npm version](https://badge.fury.io/js/structured-source.svg)](http://badge.fury.io/js/structured-source) [![Actions Status: test](https://github.com/textlint/structured-source/workflows/test/badge.svg)](https://github.com/textlint/structured-source/actions?query=workflow%3A"test") |
| apps/vscode-extension/node_modules/supports-color/readme.md | no | 76 | baf9e8e934c7d2de | # supports-color [![Build Status](https://travis-ci.org/chalk/supports-color.svg?branch=master)](https://travis-ci.org/chalk/supports-color) |
| apps/vscode-extension/node_modules/supports-hyperlinks/readme.md | no | 39 | 9f19a22393ff995f | # supports-hyperlinks |
| apps/vscode-extension/node_modules/table/node_modules/ansi-regex/readme.md | no | 78 | 3ebc0f845b1bab50 | # ansi-regex |
| apps/vscode-extension/node_modules/table/node_modules/strip-ansi/readme.md | no | 46 | cb384db30337ecec | # strip-ansi [![Build Status](https://travis-ci.org/chalk/strip-ansi.svg?branch=master)](https://travis-ci.org/chalk/strip-ansi) |
| apps/vscode-extension/node_modules/table/README.md | no | 837 | 668edb8dd2feeeee | # Table |
| apps/vscode-extension/node_modules/tar-fs/README.md | no | 165 | ebaf8360a94df232 | # tar-fs |
| apps/vscode-extension/node_modules/tar-stream/README.md | no | 168 | de7c1f91e8da68d3 | # tar-stream |
| apps/vscode-extension/node_modules/terminal-link/readme.md | no | 82 | 60b87174b95f453d | # terminal-link |
| apps/vscode-extension/node_modules/textextensions/LICENSE.md | no | 101 | 5fdbfb4ce1eb9581 | # License |
| apps/vscode-extension/node_modules/textextensions/README.md | no | 208 | 856ad67f57407f35 | # The Definitive List of Text Extensions |
| apps/vscode-extension/node_modules/textextensions/SECURITY.md | no | 21 | 3aec3ae6022ebe98 | # Security Policy |
| apps/vscode-extension/node_modules/tmp/README.md | no | 391 | efbc7bd03fbc4a64 | # Tmp |
| apps/vscode-extension/node_modules/to-regex-range/README.md | no | 305 | abab275498571b39 | # to-regex-range [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=W8YFZ425KND68) [![NPM version](https://img.shields.io/npm/v/to-regex-range.svg?style=flat)](https://www.npmjs.com/package/to-regex-range) [![NPM monthly downloads](https://img.shields.io/npm/dm/to-regex-range.svg?style=flat)](https://npmjs.org/package/to-regex-range) [![NPM total downloads](https://img.shields.io/npm/dt/to-regex-range.svg?style=flat)](https://npmjs.org/package/to-regex-range) [![Linux Build Status](https://img.shields.io/travis/micromatch/to-regex-range.svg?style=flat&label=Travis)](https://travis-ci.org/micromatch/to-regex-range) |
| apps/vscode-extension/node_modules/tslib/README.md | no | 164 | d2e199aa7eafd807 | # tslib |
| apps/vscode-extension/node_modules/tslib/SECURITY.md | no | 41 | 89c4e4b9ba7ec705 | ## Security |
| apps/vscode-extension/node_modules/tunnel-agent/README.md | no | 4 | c8086e96047bc824 | (no markdown heading) |
| apps/vscode-extension/node_modules/tunnel/CHANGELOG.md | no | 22 | f37a8ae38d10a0ea | # Changelog |
| apps/vscode-extension/node_modules/tunnel/README.md | no | 185 | 9afc542dbf47853c | # node-tunnel - HTTP/HTTPS Agents for tunneling proxies |
| apps/vscode-extension/node_modules/type-fest/readme.md | no | 1060 | 948a0391e53ff1cd | ## Install |
| apps/vscode-extension/node_modules/typed-rest-client/opensource/Node-SMB/README.md | no | 5 | 0aea28c1191c51ff | ### Reference: |
| apps/vscode-extension/node_modules/typed-rest-client/README.md | no | 106 | 14d06318afe705a9 | # Typed REST and HTTP Client with TypeScript Typings |
| apps/vscode-extension/node_modules/uc.micro/README.md | no | 14 | 005da828ae5926bd | # uc.micro |
| apps/vscode-extension/node_modules/underscore/README.md | no | 34 | 3ab10c9d25a11bf5 | (no markdown heading) |
| apps/vscode-extension/node_modules/undici/docs/docs/api/Agent.md | no | 84 | e77f5a46d93d27a7 | # Agent |
| apps/vscode-extension/node_modules/undici/docs/docs/api/api-lifecycle.md | no | 91 | 315bef8bb747c29b | # Client Lifecycle |
| apps/vscode-extension/node_modules/undici/docs/docs/api/BalancedPool.md | no | 99 | eadeec57b37da6bc | # Class: BalancedPool |
| apps/vscode-extension/node_modules/undici/docs/docs/api/CacheStorage.md | no | 30 | 37e458d8baff6586 | # CacheStorage |
| apps/vscode-extension/node_modules/undici/docs/docs/api/CacheStore.md | no | 164 | c2df38ab5a312e7b | # Cache Store |
| apps/vscode-extension/node_modules/undici/docs/docs/api/Client.md | no | 288 | 4022a398d7ac679b | # Class: Client |
| apps/vscode-extension/node_modules/undici/docs/docs/api/ClientStats.md | no | 27 | a568b57ed687a803 | # Class: ClientStats |
| apps/vscode-extension/node_modules/undici/docs/docs/api/Connector.md | no | 115 | c363feda8c4bb65f | # Connector |
| apps/vscode-extension/node_modules/undici/docs/docs/api/ContentType.md | no | 57 | b7418622c803d210 | # MIME Type Parsing |
| apps/vscode-extension/node_modules/undici/docs/docs/api/Cookies.md | no | 128 | 5510c1cac6d2b79b | # Cookie Handling |
| apps/vscode-extension/node_modules/undici/docs/docs/api/Debug.md | no | 62 | e2097e6df91877e5 | # Debug |
| apps/vscode-extension/node_modules/undici/docs/docs/api/DiagnosticsChannel.md | no | 317 | 770d93dfd812f620 | # Diagnostics Channel Support |
| apps/vscode-extension/node_modules/undici/docs/docs/api/Dispatcher.md | no | 1393 | 0ab6e9a16ac733bb | # Dispatcher |
| apps/vscode-extension/node_modules/undici/docs/docs/api/EnvHttpProxyAgent.md | no | 159 | a0eb830a46a3b42b | # Class: EnvHttpProxyAgent |
| apps/vscode-extension/node_modules/undici/docs/docs/api/Errors.md | no | 49 | 2ce5a5d33c4960b9 | # Errors |
| apps/vscode-extension/node_modules/undici/docs/docs/api/EventSource.md | no | 45 | 4f6abf7c96d473ff | # EventSource |
| apps/vscode-extension/node_modules/undici/docs/docs/api/Fetch.md | no | 60 | 0b861a7836a78316 | # Fetch |
| apps/vscode-extension/node_modules/undici/docs/docs/api/GlobalInstallation.md | no | 139 | b2f8d71146d8fe80 | # Global Installation |
| apps/vscode-extension/node_modules/undici/docs/docs/api/H2CClient.md | no | 263 | bf1f6bf6a0073158 | # Class: H2CClient |
| apps/vscode-extension/node_modules/undici/docs/docs/api/MockAgent.md | no | 603 | 2410634ae6cae9b3 | # Class: MockAgent |
| apps/vscode-extension/node_modules/undici/docs/docs/api/MockCallHistory.md | no | 197 | b059d5b2a953cd8d | # Class: MockCallHistory |
| apps/vscode-extension/node_modules/undici/docs/docs/api/MockCallHistoryLog.md | no | 43 | 3fe81715f164747a | # Class: MockCallHistoryLog |
| apps/vscode-extension/node_modules/undici/docs/docs/api/MockClient.md | no | 81 | ef57c87aab22d39f | # Class: MockClient |
| apps/vscode-extension/node_modules/undici/docs/docs/api/MockErrors.md | no | 12 | 862b81346856a128 | # MockErrors |
| apps/vscode-extension/node_modules/undici/docs/docs/api/MockPool.md | no | 555 | eadb07b70b40f1d9 | # Class: MockPool |
| apps/vscode-extension/node_modules/undici/docs/docs/api/Pool.md | no | 84 | 4919c5265b241d00 | # Class: Pool |
| apps/vscode-extension/node_modules/undici/docs/docs/api/PoolStats.md | no | 35 | eae89aa388a6cb3b | # Class: PoolStats |
| apps/vscode-extension/node_modules/undici/docs/docs/api/ProxyAgent.md | no | 229 | daff25867159019e | # Class: ProxyAgent |
| apps/vscode-extension/node_modules/undici/docs/docs/api/RedirectHandler.md | no | 93 | 0bf06eb4c1895f4e | # Class: RedirectHandler |
| apps/vscode-extension/node_modules/undici/docs/docs/api/RetryAgent.md | no | 50 | 4b2b419ff9d278e8 | # Class: RetryAgent |
| apps/vscode-extension/node_modules/undici/docs/docs/api/RetryHandler.md | no | 118 | 390712a1791393ba | # Class: RetryHandler |
| apps/vscode-extension/node_modules/undici/docs/docs/api/RoundRobinPool.md | no | 145 | 1b796f65d4126bd7 | # Class: RoundRobinPool |
| apps/vscode-extension/node_modules/undici/docs/docs/api/SnapshotAgent.md | no | 616 | 83ae2c7e9df88c9f | # SnapshotAgent |
| apps/vscode-extension/node_modules/undici/docs/docs/api/Socks5ProxyAgent.md | no | 275 | c335f2224671d055 | # Class: Socks5ProxyAgent |
| apps/vscode-extension/node_modules/undici/docs/docs/api/Util.md | no | 25 | c61bedd14de49978 | # Util |
| apps/vscode-extension/node_modules/undici/docs/docs/api/WebSocket.md | no | 141 | 9c4e9e208c803e0d | # Class: WebSocket |
| apps/vscode-extension/node_modules/undici/docs/docs/best-practices/client-certificate.md | no | 64 | f04bc4291917e454 | # Client certificate |
| apps/vscode-extension/node_modules/undici/docs/docs/best-practices/crawling.md | no | 58 | e29aef651867d2c6 | # Crawling |
| apps/vscode-extension/node_modules/undici/docs/docs/best-practices/mocking-request.md | no | 190 | 71bd60cfc22c379f | # Mocking Request |
| apps/vscode-extension/node_modules/undici/docs/docs/best-practices/proxy.md | no | 127 | e37e207295e581d9 | # Connecting through a proxy |
| apps/vscode-extension/node_modules/undici/docs/docs/best-practices/undici-vs-builtin-fetch.md | no | 224 | 255b781d22e486e3 | # Undici Module vs. Node.js Built-in Fetch |
| apps/vscode-extension/node_modules/undici/docs/docs/best-practices/writing-tests.md | no | 63 | 4c0d5a920208aa63 | # Writing tests |
| apps/vscode-extension/node_modules/undici/lib/web/subresource-integrity/Readme.md | no | 9 | 0d3da607c6e6d742 | # Subresource Integrity |
| apps/vscode-extension/node_modules/undici/README.md | no | 741 | 2c963a2f4d040fb3 | # undici |
| apps/vscode-extension/node_modules/undici/types/README.md | no | 6 | c8cced6ec588c55b | # undici-types |
| apps/vscode-extension/node_modules/unicorn-magic/readme.md | no | 25 | 968ca1b138df60e1 | # unicorn-magic |
| apps/vscode-extension/node_modules/universalify/README.md | no | 76 | 7419741d5da27174 | # universalify |
| apps/vscode-extension/node_modules/url-join/CHANGELOG.md | no | 88 | 2ad9471cc1acfe83 | ## 4.0.0 - 2018-02-02 |
| apps/vscode-extension/node_modules/url-join/README.md | no | 47 | d7cd97d6ae2b5974 | ## Install |
| apps/vscode-extension/node_modules/util-deprecate/History.md | no | 16 | ab183ff93d075137 | (no markdown heading) |
| apps/vscode-extension/node_modules/util-deprecate/README.md | no | 53 | d30a5eca847bc6ed | ### The Node.js `util.deprecate()` function with browser support |
| apps/vscode-extension/node_modules/validate-npm-package-license/README.md | no | 113 | 83d2cb7ce540025d | (no markdown heading) |
| apps/vscode-extension/node_modules/version-range/LICENSE.md | no | 101 | 5fdbfb4ce1eb9581 | # License |
| apps/vscode-extension/node_modules/version-range/README.md | no | 235 | b2d38b34fd6831ee | # version-range |
| apps/vscode-extension/node_modules/version-range/SECURITY.md | no | 21 | 261895f09e352b84 | # Security Policy |
| apps/vscode-extension/node_modules/whatwg-encoding/README.md | no | 50 | 71c292696a9fe3a4 | # Decode According to the WHATWG Encoding Standard |
| apps/vscode-extension/node_modules/whatwg-mimetype/README.md | no | 101 | 7863ccdd2d400ee7 | # Parse, serialize, and manipulate MIME types |
| apps/vscode-extension/node_modules/which/CHANGELOG.md | no | 166 | 89bc599ca0b3a119 | # Changes |
| apps/vscode-extension/node_modules/which/README.md | no | 54 | 0c91f714f46006bc | # which |
| apps/vscode-extension/node_modules/wrappy/README.md | no | 36 | 0d2537e86a9e5ae8 | # wrappy |
| apps/vscode-extension/node_modules/wsl-utils/readme.md | no | 50 | 3d5874633f3b33b8 | # wsl-utils |
| apps/vscode-extension/node_modules/xml2js/README.md | no | 507 | 2ceeb784c1265676 | ### Adding xmlns attributes |
| apps/vscode-extension/node_modules/xmlbuilder/CHANGELOG.md | no | 470 | f5d267a62a272d16 | # Change Log |
| apps/vscode-extension/node_modules/xmlbuilder/README.md | no | 86 | 0ac3e2ad69e17e31 | # xmlbuilder-js |
| apps/vscode-extension/node_modules/yallist/README.md | no | 204 | cf293896dc0c704e | # yallist |
| apps/vscode-extension/node_modules/yauzl/README.md | no | 658 | 8df92afb1e8ea3c7 | # yauzl |
| apps/vscode-extension/node_modules/yazl/README.md | no | 389 | 8c9fcb9afda0c2e6 | # yazl |
| apps/vscode-extension/README.md | yes | 83 | 3cf71126124c906a | # EOIP Context |
| apps/web/node_modules/@esbuild/win32-x64/README.md | no | 3 | 29cf512fa580b723 | # esbuild |
| apps/web/node_modules/@playwright/test/README.md | no | 168 | 5727f6f514da3922 | # 🎭 Playwright |
| apps/web/node_modules/@rollup/rollup-win32-x64-gnu/README.md | no | 3 | bba1939db0bf57b3 | # `@rollup/rollup-win32-x64-gnu` |
| apps/web/node_modules/@rollup/rollup-win32-x64-msvc/README.md | no | 3 | 9606170b2fb075c7 | # `@rollup/rollup-win32-x64-msvc` |
| apps/web/node_modules/@types/estree/README.md | no | 15 | 284daa8ee1deb294 | # Installation |
| apps/web/node_modules/@yomguithereal/helpers/README.md | no | 33 | 382ab9a59c990f2d | # Yomguithereal's helpers |
| apps/web/node_modules/cytoscape/.github/ISSUE_TEMPLATE/bug_report.md | no | 64 | 18f46f5b63f29ced | (no markdown heading) |
| apps/web/node_modules/cytoscape/.github/ISSUE_TEMPLATE/feature_request.md | no | 30 | 2173635bead46d5a | (no markdown heading) |
| apps/web/node_modules/cytoscape/.github/PULL_REQUEST_TEMPLATE.md | no | 29 | 740cc81a33cd8d5c | (no markdown heading) |
| apps/web/node_modules/cytoscape/.github/SECURITY.md | no | 9 | e23a16506c926d78 | # Reporting security issues in Cytoscape.js |
| apps/web/node_modules/cytoscape/.github/workflows/md/blog-issue-template.md | no | 27 | 0c8b89397f5c0193 | ## Create Issue for new release |
| apps/web/node_modules/cytoscape/.github/workflows/md/Manual_Release.md | no | 38 | f9712074820be472 | ## Manual release instructions |
| apps/web/node_modules/cytoscape/.github/workflows/md/Release.md | no | 60 | 340a4e5e5d4aabf6 | # Release GitHub Action - README |
| apps/web/node_modules/cytoscape/.github/workflows/md/repo-setup.md | no | 32 | 61d203a503de90b2 | ## Instructions to setup repository for automated releases |
| apps/web/node_modules/cytoscape/AGENTS.md | no | 69 | 86c79df5d3a68ddf | # Cytoscape.js AGENTS.md |
| apps/web/node_modules/cytoscape/CODE_OF_CONDUCT.md | no | 128 | 536d81e0f977d25f | # Contributor Covenant Code of Conduct |
| apps/web/node_modules/cytoscape/README.md | no | 172 | d76cc17e7f9ca5ca | # Cytoscape.js |
| apps/web/node_modules/esbuild/LICENSE.md | no | 21 | b40ec5baec7bb34f | (no markdown heading) |
| apps/web/node_modules/esbuild/README.md | no | 3 | 6d481cd60ec3c679 | # esbuild |
| apps/web/node_modules/events/History.md | no | 118 | 10735f184ed358cf | # 3.3.0 |
| apps/web/node_modules/events/Readme.md | no | 50 | abcf6084be683da8 | # events [![Build Status](https://travis-ci.org/Gozala/events.png?branch=master)](https://travis-ci.org/Gozala/events) |
| apps/web/node_modules/events/security.md | no | 10 | 612dfd309edc618a | # Security Policy |
| apps/web/node_modules/fdir/README.md | no | 91 | 99ba9a269bf78c24 | ## 🚄 Quickstart |
| apps/web/node_modules/graphology-types/README.md | no | 9 | d9eb2af325f216d9 | # Graphology Types |
| apps/web/node_modules/graphology-utils/README.md | no | 274 | 9ec7dfee93962355 | # Graphology Utils |
| apps/web/node_modules/graphology/README.md | no | 9 | f67ad77c5083390d | # Graphology |
| apps/web/node_modules/nanoid/README.md | no | 39 | 54449254570e72b9 | # Nano ID |
| apps/web/node_modules/obliterator/README.md | no | 415 | e440443d703b3396 | # Obliterator |
| apps/web/node_modules/picocolors/README.md | no | 21 | 5027b2836551ea0f | # picocolors |
| apps/web/node_modules/picomatch/README.md | no | 743 | a69b87120fe2b9cb | ## Why picomatch? |
| apps/web/node_modules/playwright-core/README.md | no | 3 | d16ff7f8e38fa1fc | # playwright-core |
| apps/web/node_modules/playwright/README.md | no | 168 | 5727f6f514da3922 | # 🎭 Playwright |
| apps/web/node_modules/postcss/README.md | no | 27 | 92b501afb100c2e7 | # PostCSS |
| apps/web/node_modules/react-dom/README.md | no | 60 | 80589e00067a57cb | # `react-dom` |
| apps/web/node_modules/react/README.md | no | 37 | faf7a5814bedadb9 | # `react` |
| apps/web/node_modules/rollup/LICENSE.md | no | 679 | fa1bd040c5bdeefe | # Rollup core license |
| apps/web/node_modules/rollup/README.md | no | 134 | 509a34b064a1698f | ## Overview |
| apps/web/node_modules/scheduler/README.md | no | 9 | e2f3a22fb7e2e18f | # `scheduler` |
| apps/web/node_modules/sigma/CHANGELOG.md | no | 134 | e90ba65b13f56db5 | # sigma.js - changelog: |
| apps/web/node_modules/sigma/CONTRIBUTING.md | no | 87 | 044cbb03834fd20a | # Contributor Guide |
| apps/web/node_modules/sigma/README.md | no | 84 | dae251795c3b5114 | # Sigma.js |
| apps/web/node_modules/source-map-js/README.md | no | 765 | 8e1a57daf01cd2fc | # Source Map JS |
| apps/web/node_modules/tinyglobby/README.md | no | 25 | 657d808498dddf2e | # tinyglobby |
| apps/web/node_modules/vite/LICENSE.md | no | 2120 | a77a1c089806b39a | # Vite core license |
| apps/web/node_modules/vite/README.md | no | 20 | 223635a2336dd42a | # Vite ⚡ |
| checklist.md | yes | 112 | 25391d02c12abc2e | # EOIP Coordination and Completion Checklist |
| context.md | yes | 98 | 879fa7625e9dc9a4 | # EOIP Current Coordination Context |
| demo/autodemo/README.md | yes | 158 | 1d668daf381358c7 | # EOIP client demonstrations |
| demo/autodemo/runtime-validation-report.md | yes | 68 | 9adc5a0f7b3dc0e7 | # VS Code Auto-Demo Validation |
| demo/demodata/code/README.md | yes | 52 | 7e943d98fcee1ac8 | # Code Graph Demo Data — Meridian Financial Services |
| demo/demodata/core/demo-repo/README.md | yes | 4 | b23a7c8fb1478172 | # EOIP-1 requirement trace |
| demo/demodata/crawler/README.md | yes | 48 | b91e6d798dca0744 | # Crawler Demo Data — Meridian Financial Services |
| demo/demodata/enterprise/README.md | yes | 63 | 11ee286a9add3da0 | # Northstar enterprise demo pack |
| demo/demodata/enterprise/wiki/checkout-latency-runbook.md | yes | 12 | bd18c1105504516c | # Checkout latency incident runbook |
| demo/demodata/enterprise/wiki/checkout-risk-architecture.md | yes | 34 | d95bc157842bc188 | # Checkout risk architecture |
| demo/demodata/manual/README.md | yes | 56 | b3829afdbcf01b5d | # Manual Demo Data - Meridian Financial Services (MFS) |
| demo/demodata/pipelines/README.md | yes | 82 | 67bea39b3773a571 | # Pipeline Demo Data — MFS Fraud Detection Platform |
| demo/script/walkthrough.md | yes | 489 | 5f5f3e7254537a37 | # EOIP Demo Walkthrough — Meridian Financial Services |
| docs/61-demo-playbook.md | yes | 233 | 808a97917f3de213 | # EOIP Demo Playbook |
| docs/adr-001-g2-contract-and-revision-model.md | yes | 48 | 1afbc69c00c69abf | # ADR-001: G2 source-event compatibility and revision model |
| docs/agents.md | yes | 214 | 348a089528b2a552 | # EOIP Agent Framework |
| docs/api-reference.md | yes | 293 | fe2d74be22c15cf4 | # EOIP API Reference |
| docs/application-audit-2026-10-02.md | yes | 76 | 351a4153a642b49a | # EOIP application audit |
| docs/audit-2026-10-06/assessed-gap-report.md | yes | 712 | 001c9ca30ba24bcc | # EOIP Assessed Gap Report |
| docs/audit-2026-10-06/detailed-requirements-report.md | yes | 57 | 82b0ce6403cdf2f0 | # EOIP Detailed Requirements Report |
| docs/audit-2026-10-06/phase-by-phase-implementation-approach.md | yes | 51 | a6bf00de05eda563 | # EOIP Phase-by-Phase Implementation Approach |
| docs/benchmarking.md | yes | 105 | 15ebeb27a54285f8 | # EOIP benchmark guide |
| docs/code-graph.md | yes | 198 | 6e54f21cf9e13494 | # EOIP Code Graph |
| docs/connectors-github.md | yes | 85 | 19d971d6a082e7fe | # GitHub connector |
| docs/connectors-gitlab.md | yes | 109 | 11c2dbe114b85660 | # GitLab connector |
| docs/connectors.md | yes | 193 | 023fcb1c0490c6c6 | # EOIP Source Connectors |
| docs/deep-agents-xai.md | yes | 55 | dccf5e87c524afc4 | # Governed Deep Agents and XAI |
| docs/demo-readiness-audit-2026-10-03.md | yes | 178 | dd56654c7f860ee7 | # EOIP enterprise demo-readiness audit |
| docs/deployment-ha.md | yes | 139 | 3ea59455ba114a50 | # EOIP High-Availability Deployment |
| docs/deployment-verification.md | yes | 35 | b41441c81d4d43fe | # Local deployment verification |
| docs/docker-local.md | yes | 748 | bba8d1b6778f346f | # Local Docker deployment |
| docs/eoip-development-audit-2026-10-03.md | yes | 563 | 74411c7ce969e82d | # EOIP Development and Demo-Readiness Audit |
| docs/file-parsing.md | yes | 195 | 135dc56618bb8f9e | # Actual file parsing and ingestion |
| docs/g2-traceability.md | yes | 64 | 511116e6579f367b | # G2 implementation traceability |
| docs/gap-audit-2026-10-02.md | yes | 637 | 988d4d87d59f3927 | # EOIP implementation gap audit & prioritized backlog |
| docs/graph-algorithms.md | yes | 210 | 11eaaeba82fcd2a4 | # EOIP Graph Algorithms |
| docs/hubble-local.md | yes | 224 | 2b4bb14ee5414b6c | # Hubble Basics + standalone RocksDB |
| docs/hubble-runtime-validation.md | yes | 441 | 81ce2c1021bafe9b | # Hubble Runtime Validation Report |
| docs/ingestion.md | yes | 239 | b0379195968be509 | # EOIP Ingestion Pipeline |
| docs/ontology.md | yes | 249 | e8ecb9fd3244f1cc | # EOIP Ontology |
| docs/phase-completion-audit-2026-10-03.md | yes | 400 | 1d800705701bf92f | # EOIP/KnowGridFlow — Phase Completion Audit Checklist |
| docs/query-engine.md | yes | 220 | 8b9eb7c9596ae1a8 | # EOIP Query Engine |
| docs/rag.md | yes | 196 | 3e2d4d4fdc38ad45 | # EOIP GraphRAG Retrieval System |
| docs/validation-evidence-phase1.md | yes | 92 | 80072c222615f24c | # Audit phase 1: validation evidence foundation |
| EOIP-engg-doc-pkg/00-specification-audit-and-enhancements.md | yes | 108 | 4084401be2f9b048 | # Specification Audit and Requirement Enhancements |
| EOIP-engg-doc-pkg/01-project-vision.md | yes | 42 | a9f4126e7cda138e | # Project Vision |
| EOIP-engg-doc-pkg/02-scope-and-objectives.md | yes | 42 | da8fc1ec0fa54030 | # Scope and Objectives |
| EOIP-engg-doc-pkg/03-functional-requirements.md | yes | 683 | 64cb376f0dbe2231 | # Functional Requirements |
| EOIP-engg-doc-pkg/04-non-functional-requirements.md | yes | 171 | 320a62c9ffdb4729 | # Non-Functional Requirements |
| EOIP-engg-doc-pkg/05-system-requirements.md | yes | 42 | 4c873fc951d3b2b0 | # System Requirements |
| EOIP-engg-doc-pkg/06-architecture.md | yes | 333 | 378ea79b522f93f1 | # Target Architecture |
| EOIP-engg-doc-pkg/07-component-architecture.md | yes | 72 | d3a24cfb3b2ed58d | # Component Architecture |
| EOIP-engg-doc-pkg/08-deployment-architecture.md | yes | 79 | 9d51ccb4232b1759 | # Deployment Architecture |
| EOIP-engg-doc-pkg/09-data-architecture.md | yes | 44 | 61d1dcff86d4f1c9 | # Data Architecture |
| EOIP-engg-doc-pkg/10-enterprise-ontology.md | yes | 40 | 575ab79dc9c8a8ce | # Enterprise Ontology |
| EOIP-engg-doc-pkg/11-graph-schema.md | yes | 62 | fe22f215c4a66449 | # HugeGraph Graph Schema |
| EOIP-engg-doc-pkg/12-meta-graph-design.md | yes | 40 | 6341b6e7c1b9ba8a | # Meta Graph Design |
| EOIP-engg-doc-pkg/13-relationship-model.md | yes | 40 | 1f05151a7643b0be | # Relationship Model |
| EOIP-engg-doc-pkg/14-temporal-graph.md | yes | 39 | f01e0612210929d5 | # Temporal Graph |
| EOIP-engg-doc-pkg/15-provenance-lineage.md | yes | 40 | dab70baf28956a5c | # Provenance and Lineage |
| EOIP-engg-doc-pkg/16-identity-resolution.md | yes | 39 | 830ae3dd340aa98b | # Identity Resolution |
| EOIP-engg-doc-pkg/17-code-graph.md | yes | 42 | d91b112a87f4ba9b | # Code Graph |
| EOIP-engg-doc-pkg/18-ingestion-architecture.md | yes | 53 | 3e93ca3b2205284a | # Ingestion Architecture |
| EOIP-engg-doc-pkg/19-connector-framework.md | yes | 41 | b1e1d92bc0f14632 | # Connector Framework |
| EOIP-engg-doc-pkg/20-jira-connector-requirements.md | yes | 39 | 03ece9c052dffe27 | # Jira Connector Requirements |
| EOIP-engg-doc-pkg/21-confluence-connector-requirements.md | yes | 38 | 91eb356b39a6e57f | # Confluence Connector Requirements |
| EOIP-engg-doc-pkg/22-gitlab-connector-requirements.md | yes | 40 | 97b43c085178485d | # Git/GitLab Connector Requirements |
| EOIP-engg-doc-pkg/23-servicenow-connector-requirements.md | yes | 38 | fad7d4bb88d6979b | # ServiceNow Connector Requirements |
| EOIP-engg-doc-pkg/24-file-web-connectors.md | yes | 42 | eb3eba2f719d6c98 | # File and Intranet Connector Requirements |
| EOIP-engg-doc-pkg/25-query-engine-requirements.md | yes | 57 | d9d5bf16ceec79b4 | # Query Engine Requirements |
| EOIP-engg-doc-pkg/26-query-engine-implementation.md | yes | 66 | 3a1c64f75138a2db | # Query Engine Implementation |
| EOIP-engg-doc-pkg/27-ontology-validation.md | yes | 39 | 60d4bf8611772fde | # Ontology Validation |
| EOIP-engg-doc-pkg/28-graph-quality.md | yes | 39 | fca6db75053af9c4 | # Graph Quality |
| EOIP-engg-doc-pkg/29-rag-architecture.md | yes | 58 | 5e54064da716a275 | # RAG Architecture |
| EOIP-engg-doc-pkg/30-agent-architecture.md | yes | 61 | c3ed1557a759f09a | # Agent Architecture |
| EOIP-engg-doc-pkg/31-multi-agent-architecture.md | yes | 40 | eef840078cfd3b73 | # Multi-Agent Architecture |
| EOIP-engg-doc-pkg/32-memory-engineering.md | yes | 39 | 88ecb00f48144b36 | # Memory Engineering |
| EOIP-engg-doc-pkg/33-context-engineering.md | yes | 42 | c84989bb7e3d445e | # Context Engineering |
| EOIP-engg-doc-pkg/34-loop-engineering.md | yes | 38 | 99365da1f8722607 | # Loop Engineering |
| EOIP-engg-doc-pkg/35-graph-engineering.md | yes | 42 | 32bd915a1f0ecda5 | # Graph Engineering |
| EOIP-engg-doc-pkg/36-harness-engineering.md | yes | 42 | 96bab7392e47c670 | # Harness Engineering |
| EOIP-engg-doc-pkg/37-graph-over-loop.md | yes | 41 | d24e82f0ba204915 | # Graph-over-Loop Engineering |
| EOIP-engg-doc-pkg/38-loop-over-graph.md | yes | 40 | 485afc1c22f72037 | # Loop-over-Graph Engineering |
| EOIP-engg-doc-pkg/39-mcp-architecture.md | yes | 40 | 8b6b87c21af8527f | # MCP Architecture |
| EOIP-engg-doc-pkg/40-human-control-model.md | yes | 39 | bded93a051cefc64 | # Human Control Model |
| EOIP-engg-doc-pkg/41-xai-explainability.md | yes | 40 | 6ca04e7069563b68 | # XAI and Explainability |
| EOIP-engg-doc-pkg/42-web-user-ui-ux.md | yes | 40 | e132992f6e40fc08 | # Web User UI/UX |
| EOIP-engg-doc-pkg/43-admin-ui-ux.md | yes | 43 | 51418136f2da9db1 | # Admin UI/UX |
| EOIP-engg-doc-pkg/44-vscode-extension.md | yes | 42 | 2fa124c6b2cbdf3d | # VS Code Extension |
| EOIP-engg-doc-pkg/45-api-specification.md | yes | 43 | 0490c01bc97d2f6a | # API Specification |
| EOIP-engg-doc-pkg/46-security-architecture.md | yes | 56 | ad4920a094b72336 | # Security Architecture |
| EOIP-engg-doc-pkg/47-threat-model.md | yes | 49 | 99300cd99900462c | # Threat Model |
| EOIP-engg-doc-pkg/48-data-privacy.md | yes | 40 | 0552010a6a511631 | # Data Privacy |
| EOIP-engg-doc-pkg/49-local-ai-model-strategy.md | yes | 40 | de1cb70f9ff2fbd6 | # Local AI Model Strategy |
| EOIP-engg-doc-pkg/50-observability.md | yes | 38 | 6970b55ea4e5c583 | # Observability |
| EOIP-engg-doc-pkg/51-performance.md | yes | 45 | 5f805a1ef26d4601 | # Performance Engineering |
| EOIP-engg-doc-pkg/52-scalability.md | yes | 40 | 78f1f8edf18cec3d | # Scalability |
| EOIP-engg-doc-pkg/53-backup-restore.md | yes | 38 | 8f0c89d7fdae0847 | # Backup and Restore |
| EOIP-engg-doc-pkg/54-devsecops.md | yes | 40 | 0b2828d21715beb0 | # DevSecOps |
| EOIP-engg-doc-pkg/55-testing-strategy.md | yes | 110 | 8144dd3192640122 | # Testing Strategy |
| EOIP-engg-doc-pkg/56-rag-agent-evaluation.md | yes | 42 | c1c60235456e071c | # RAG and Agent Evaluation |
| EOIP-engg-doc-pkg/57-graph-validation-test-plan.md | yes | 43 | 56db120b4aa616ee | # Graph Validation Test Plan |
| EOIP-engg-doc-pkg/58-end-to-end-test-plan.md | yes | 42 | b9455a372b8783b3 | # End-to-End Test Plan |
| EOIP-engg-doc-pkg/59-docker-deployment.md | yes | 64 | eb03176662a12d24 | # Docker Deployment |
| EOIP-engg-doc-pkg/60-operational-runbook.md | yes | 41 | ef9949f7fbdf855c | # Operational Runbook |
| EOIP-engg-doc-pkg/61-demo-playbook.md | yes | 61 | ebaeaf581099c518 | # Demo Playbook |
| EOIP-engg-doc-pkg/62-risk-register.md | yes | 27 | 03d8a989d2d5c6a0 | # Risk Register |
| EOIP-engg-doc-pkg/63-assumptions.md | yes | 31 | 7aa01411ac203d6c | # Assumptions |
| EOIP-engg-doc-pkg/64-decisions-and-adrs.md | yes | 39 | 56297c0d7fa2ad13 | # Architecture Decisions and ADRs |
| EOIP-engg-doc-pkg/65-glossary.md | yes | 50 | adb5755791eb1298 | # Glossary |
| EOIP-engg-doc-pkg/66-phase-roadmap.md | yes | 64 | 0abe43097d378431 | # Phased Roadmap |
| EOIP-engg-doc-pkg/67-implementation-plan.md | yes | 265 | a1f98fb4bf0f5b95 | # Master Implementation Plan |
| EOIP-engg-doc-pkg/68-project-structure.md | yes | 87 | 65a6a5522f63778f | # Project Structure |
| EOIP-engg-doc-pkg/69-dependency-license-sbom.md | yes | 37 | 786168e188b0f10a | # Dependency, License and SBOM |
| EOIP-engg-doc-pkg/70-acceptance-criteria.md | yes | 131 | 0e81f7132284033c | # Acceptance Criteria |
| EOIP-engg-doc-pkg/71-research-and-verification-basis.md | yes | 31 | 566fe15c918c8ef0 | # Research and Verification Basis |
| EOIP-engg-doc-pkg/72-requirement-traceability.md | yes | 128 | 0befd674dec4ccad | # Requirement Traceability Matrix |
| EOIP-engg-doc-pkg/73-architecture-diagrams.md | yes | 293 | 093459aac532aaca | # Architecture Diagram Catalog |
| EOIP-engg-doc-pkg/74-data-contracts.md | yes | 209 | c15dbe1425373dbc | # Data Contracts |
| EOIP-engg-doc-pkg/75-self-review-and-gap-closure.md | yes | 40 | fef0185d9760b222 | # Architecture Self-Review and Gap Closure |
| EOIP-engg-doc-pkg/76-multi-backend.md | yes | 179 | e81496b6a52ee043 | # EOIP Multi-Backend GraphStore |
| EOIP-engg-doc-pkg/diagrams/01-system-context.md | yes | 18 | 6f847a1ba8b1d0aa | # 01-system-context |
| EOIP-engg-doc-pkg/diagrams/02-container-architecture.md | yes | 24 | c31b925367eaf0ef | # 02-container-architecture |
| EOIP-engg-doc-pkg/diagrams/03-ingestion-pipeline.md | yes | 10 | f5f4117822eb038b | # 03-ingestion-pipeline |
| EOIP-engg-doc-pkg/diagrams/04-enterprise-graph-architecture.md | yes | 17 | 2d71f91e5ff70a90 | # 04-enterprise-graph-architecture |
| EOIP-engg-doc-pkg/diagrams/05-meta-graph.md | yes | 14 | 909fc44ec2001519 | # 05-meta-graph |
| EOIP-engg-doc-pkg/diagrams/06-code-graph.md | yes | 12 | d6034dd75433ab01 | # 06-code-graph |
| EOIP-engg-doc-pkg/diagrams/07-cross-domain-relationship-graph.md | yes | 15 | 5cdc57d4e6d4a79f | # 07-cross-domain-relationship-graph |
| EOIP-engg-doc-pkg/diagrams/08-query-execution.md | yes | 14 | ed8bfa064f74d3f9 | # 08-query-execution |
| EOIP-engg-doc-pkg/diagrams/09-graphrag.md | yes | 14 | 0510787faaeba3f9 | # 09-graphrag |
| EOIP-engg-doc-pkg/diagrams/10-agent-runtime.md | yes | 18 | 34383ce35fa2b472 | # 10-agent-runtime |
| EOIP-engg-doc-pkg/diagrams/11-multi-agent-orchestration.md | yes | 17 | 1e88f82099e5e7da | # 11-multi-agent-orchestration |
| EOIP-engg-doc-pkg/diagrams/12-mcp-architecture.md | yes | 12 | 7af6721c67e1ed4a | # 12-mcp-architecture |
| EOIP-engg-doc-pkg/diagrams/13-human-control-architecture.md | yes | 13 | 62be85ba2c9a6bd6 | # 13-human-control-architecture |
| EOIP-engg-doc-pkg/diagrams/14-web-ui-architecture.md | yes | 14 | f11f4edb2ed1f5df | # 14-web-ui-architecture |
| EOIP-engg-doc-pkg/diagrams/15-vscode-architecture.md | yes | 12 | 51803364d8f3c76b | # 15-vscode-architecture |
| EOIP-engg-doc-pkg/diagrams/16-deployment.md | yes | 21 | 8cf441ee2cbbe9e5 | # 16-deployment |
| EOIP-engg-doc-pkg/diagrams/17-mvp-e2e-flow.md | yes | 22 | e5e469cde30763ee | # 17-mvp-e2e-flow |
| EOIP-engg-doc-pkg/DOCUMENTATION-INDEX.md | yes | 101 | e492b6fae9836855 | # Documentation Index |
| EOIP-engg-doc-pkg/examples/demo_documentation.md | yes | 3 | 66c5a2431dd62e82 | # EOIP-123 Impact Analysis |
| EOIP-engg-doc-pkg/gaps-implementation.md | yes | 1216 | 48286e54a0776ce4 | # gaps-implementation.md |
| EOIP-engg-doc-pkg/gaps-requirements.md | yes | 1401 | 76ed4843e3f32f69 | # gaps-requirements.md |
| EOIP-engg-doc-pkg/gaps2-implementation.md | yes | 1625 | 610101b8885c55b8 | # gaps2-implementation.md |
| EOIP-engg-doc-pkg/gaps2-requirements.md | yes | 2059 | dfb9b47bbf3cfb25 | # gaps2-requirements.md |
| EOIP-engg-doc-pkg/implementation/wp-agent-memory.md | yes | 77 | 9f72fc15038d4cff | # WP-AGENT-MEMORY Implementation Plan |
| EOIP-engg-doc-pkg/implementation/wp-codegraph.md | yes | 67 | 69f1742ee7be7eec | # WP-CODEGRAPH Implementation Plan |
| EOIP-engg-doc-pkg/implementation/wp-connectors.md | yes | 107 | d088338c0da4e9e6 | # WP-CONNECTORS Implementation Plan |
| EOIP-engg-doc-pkg/implementation/wp-experience.md | yes | 77 | 7387b1b6dbce48a2 | # WP-EXPERIENCE Implementation Plan |
| EOIP-engg-doc-pkg/implementation/wp-foundation.md | yes | 67 | f3e58f7181d30a75 | # WP-FOUNDATION Implementation Plan |
| EOIP-engg-doc-pkg/implementation/wp-ingestion.md | yes | 67 | 32732c84523978b4 | # WP-INGESTION Implementation Plan |
| EOIP-engg-doc-pkg/implementation/wp-mcp.md | yes | 37 | 8c7ee26a187fc1be | # WP-MCP Implementation Plan |
| EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md | yes | 137 | 05ccb1b4a514712c | # WP-ONTOLOGY-GRAPH Implementation Plan |
| EOIP-engg-doc-pkg/implementation/wp-query.md | yes | 107 | 16ead715beffd155 | # WP-QUERY Implementation Plan |
| EOIP-engg-doc-pkg/implementation/wp-rag.md | yes | 77 | 3d55d1cac4ad980d | # WP-RAG Implementation Plan |
| EOIP-engg-doc-pkg/implementation/wp-security-ops.md | yes | 157 | 2ddae9a952d1bd7c | # WP-SECURITY-OPS Implementation Plan |
| EOIP-engg-doc-pkg/implementation/wp-validation.md | yes | 47 | ed959d83ce6d3163 | # WP-VALIDATION Implementation Plan |
| EOIP-engg-doc-pkg/KGR-implementation-plan.md | yes | 2838 | 863c5bac10c21f2d | # KGR — Knowledge Graph Renderer: Phase-by-Phase Implementation Plan |
| EOIP-engg-doc-pkg/KGR-requirements.md | yes | 1145 | 923ea7e8acea158f | # KGR — Knowledge Graph Renderer & Explorer: Requirements Specification |
| EOIP-engg-doc-pkg/knowgridflow-product-architecture.md | yes | 2010 | 40549755cc02fb22 | # KnowGridFlow Product Architecture |
| EOIP-engg-doc-pkg/MVP-implementation-plan.md | yes | 590 | f47280f32166d976 | # MVP Implementation Plan |
| EOIP-engg-doc-pkg/MVP-requirements.md | yes | 275 | 18ab7fb37df6b910 | # MVP Requirements |
| EOIP-engg-doc-pkg/README.md | yes | 49 | fa49b45b12511926 | # Enterprise Ontology & Intelligence Platform (EOIP) — Engineering Documentation Package |
| examples/demo-enterprise/README.md | yes | 28 | d0d1e3a5fe417883 | # Northstar enterprise demo pack |
| examples/demo-enterprise/wiki/checkout-latency-runbook.md | yes | 12 | bd18c1105504516c | # Checkout latency incident runbook |
| examples/demo-enterprise/wiki/checkout-risk-architecture.md | yes | 34 | d95bc157842bc188 | # Checkout risk architecture |
| examples/demo-repo/README.md | yes | 4 | b23a7c8fb1478172 | # EOIP-1 requirement trace |
| handoff_template.md | yes | 39 | 414c79298224ac20 | # EOIP Handoff Template |
| instruction.md | yes | 140 | 60e70b0d3ede0845 | # EOIP Agent Orchestration Instructions and Contracts |
| memory.md | yes | 326 | c3e3e53d2216bb17 | # EOIP Coordination Memory |
| onboarding_checklist.md | yes | 27 | e471f62f5d43279c | # EOIP Onboarding Checklist |
| onboarding_prompts.md | yes | 71 | 5683270bbb484534 | # EOIP Onboarding and Resume Prompts |
| README.md | yes | 117 | de063f7145110438 | # EOIP — Enterprise Ontology & Intelligence Platform |
| roles.md | yes | 526 | c28e5068f007c156 | # EOIP Application Roles, Activities and Persona Lines |
| secrets.example/README.md | yes | 24 | a8feb4a87029e4fb | # Secrets Directory |
| test-results/application-login-search-t-c1db8-d-administer-persisted-data/error-context.md | no | 330 | 9403d2b2147c4275 | # Page snapshot |
| tickets/requirements-map.md | yes | 28 | b1298e7d2c2830f6 | # EOIP Requirements and Coordination Map |
| tickets/ticket-20261004-001.md | yes | 83 | 2f7fca404abf1f6e | ## Reconciliation - 2026-10-04 |
| tickets/ticket-20261004-002.md | yes | 61 | c678640944c63915 | (no markdown heading) |
| tickets/ticket-20261004-003.md | yes | 110 | 21ad600d2671b653 | (no markdown heading) |
| tickets/ticket-20261004-004.md | yes | 66 | 67ae81d49e282cdb | ## Verified gap and scope |
| tickets/ticket-20261004-005.md | yes | 109 | b90cd30f943b1649 | (no markdown heading) |
| tickets/ticket-template.md | yes | 38 | 01a97139f1c81bf2 | # EOIP Ticket Template |
| todo-status.md | yes | 33 | 949d82469a6a472d | # EOIP Ticket Queue |

## Audit JSON Summary

| Audit file | Requirements | Done | Partial | Planned | Done ratio | Gate passed |
| --- | --- | --- | --- | --- | --- | --- |
| gap-coverage-audit.json | 296 | 296 | 0 | 0 | 1.0 | True |
| g2-coverage-audit.json | 364 | 364 | 0 | 0 | 1.0 | True |

Truth note: both supplied JSON audit files report 100% `done` and passing gates. That is useful traceability evidence, but the codebase still needs normal release validation for security posture, scale limits, client-specific graph database behavior, and production acceptance in the target environment.

## Document Families

| Family / Top-level path | Markdown files |
| --- | --- |
| EOIP-engg-doc-pkg | 118 |
| README.md | 1 |
| agent_runbook.md | 1 |
| apps | 1 |
| checklist.md | 1 |
| context.md | 1 |
| demo | 11 |
| docs | 31 |
| examples | 4 |
| handoff_template.md | 1 |
| instruction.md | 1 |
| memory.md | 1 |
| onboarding_checklist.md | 1 |
| onboarding_prompts.md | 1 |
| roles.md | 1 |
| secrets.example | 1 |
| tickets | 7 |
| todo-status.md | 1 |

## Source Document Manifest

Every project-authored Markdown file in scope is listed below with line count, content hash prefix, first heading, and line-analysis counters. The `Audit JSON refs` column shows how many supplied audit requirements point directly at that file.

| Markdown source | Lines | SHA-256 prefix | First heading | Headings | Req-like | Status-like | Audit JSON refs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| agent_runbook.md | 83 | 0e916fd7a4cf5e61 | # EOIP Agent Runbook | 4 | 22 | 4 | 0 |
| apps/vscode-extension/README.md | 83 | 3cf71126124c906a | # EOIP Context | 1 | 20 | 0 | 0 |
| checklist.md | 112 | 25391d02c12abc2e | # EOIP Coordination and Completion Checklist | 6 | 34 | 15 | 0 |
| context.md | 98 | 879fa7625e9dc9a4 | # EOIP Current Coordination Context | 5 | 27 | 6 | 0 |
| demo/autodemo/README.md | 158 | 1d668daf381358c7 | # EOIP client demonstrations | 5 | 46 | 7 | 0 |
| demo/autodemo/runtime-validation-report.md | 68 | 9adc5a0f7b3dc0e7 | # VS Code Auto-Demo Validation | 3 | 16 | 0 | 0 |
| demo/demodata/code/README.md | 52 | 7e943d98fcee1ac8 | # Code Graph Demo Data — Meridian Financial Services | 5 | 5 | 0 | 0 |
| demo/demodata/core/demo-repo/README.md | 4 | b23a7c8fb1478172 | # EOIP-1 requirement trace | 1 | 1 | 0 | 0 |
| demo/demodata/crawler/README.md | 48 | b91e6d798dca0744 | # Crawler Demo Data — Meridian Financial Services | 4 | 10 | 1 | 0 |
| demo/demodata/enterprise/README.md | 63 | 11ee286a9add3da0 | # Northstar enterprise demo pack | 4 | 16 | 3 | 0 |
| demo/demodata/enterprise/wiki/checkout-latency-runbook.md | 12 | bd18c1105504516c | # Checkout latency incident runbook | 1 | 3 | 0 | 0 |
| demo/demodata/enterprise/wiki/checkout-risk-architecture.md | 34 | d95bc157842bc188 | # Checkout risk architecture | 6 | 5 | 5 | 0 |
| demo/demodata/manual/README.md | 56 | b3829afdbcf01b5d | # Manual Demo Data - Meridian Financial Services (MFS) | 6 | 8 | 0 | 0 |
| demo/demodata/pipelines/README.md | 82 | 67bea39b3773a571 | # Pipeline Demo Data — MFS Fraud Detection Platform | 7 | 4 | 2 | 0 |
| demo/script/walkthrough.md | 489 | 5f5f3e7254537a37 | # EOIP Demo Walkthrough — Meridian Financial Services | 63 | 88 | 3 | 0 |
| docs/61-demo-playbook.md | 233 | 808a97917f3de213 | # EOIP Demo Playbook | 33 | 74 | 9 | 0 |
| docs/adr-001-g2-contract-and-revision-model.md | 48 | 1afbc69c00c69abf | # ADR-001: G2 source-event compatibility and revision model | 4 | 11 | 1 | 0 |
| docs/agents.md | 214 | 348a089528b2a552 | # EOIP Agent Framework | 29 | 27 | 4 | 0 |
| docs/api-reference.md | 293 | fe2d74be22c15cf4 | # EOIP API Reference | 49 | 64 | 2 | 0 |
| docs/application-audit-2026-10-02.md | 76 | 351a4153a642b49a | # EOIP application audit | 7 | 36 | 4 | 0 |
| docs/audit-2026-10-06/assessed-gap-report.md | 712 | 001c9ca30ba24bcc | # EOIP Assessed Gap Report | 50 | 241 | 262 | 0 |
| docs/audit-2026-10-06/detailed-requirements-report.md | 57 | 82b0ce6403cdf2f0 | # EOIP Detailed Requirements Report | 5 | 14 | 21 | 0 |
| docs/audit-2026-10-06/phase-by-phase-implementation-approach.md | 51 | a6bf00de05eda563 | # EOIP Phase-by-Phase Implementation Approach | 5 | 20 | 15 | 0 |
| docs/benchmarking.md | 105 | 15ebeb27a54285f8 | # EOIP benchmark guide | 5 | 12 | 1 | 0 |
| docs/code-graph.md | 198 | 6e54f21cf9e13494 | # EOIP Code Graph | 18 | 14 | 1 | 0 |
| docs/connectors-github.md | 85 | 19d971d6a082e7fe | # GitHub connector | 6 | 12 | 0 | 0 |
| docs/connectors-gitlab.md | 109 | 11c2dbe114b85660 | # GitLab connector | 5 | 15 | 0 | 0 |
| docs/connectors.md | 193 | 023fcb1c0490c6c6 | # EOIP Source Connectors | 34 | 37 | 0 | 0 |
| docs/deep-agents-xai.md | 55 | dccf5e87c524afc4 | # Governed Deep Agents and XAI | 7 | 17 | 2 | 0 |
| docs/demo-readiness-audit-2026-10-03.md | 178 | dd56654c7f860ee7 | # EOIP enterprise demo-readiness audit | 10 | 70 | 18 | 0 |
| docs/deployment-ha.md | 139 | 3ea59455ba114a50 | # EOIP High-Availability Deployment | 11 | 35 | 7 | 0 |
| docs/deployment-verification.md | 35 | b41441c81d4d43fe | # Local deployment verification | 1 | 19 | 0 | 0 |
| docs/docker-local.md | 748 | bba8d1b6778f346f | # Local Docker deployment | 19 | 231 | 23 | 0 |
| docs/eoip-development-audit-2026-10-03.md | 563 | 74411c7ce969e82d | # EOIP Development and Demo-Readiness Audit | 29 | 256 | 85 | 0 |
| docs/file-parsing.md | 195 | 135dc56618bb8f9e | # Actual file parsing and ingestion | 7 | 28 | 2 | 0 |
| docs/g2-traceability.md | 64 | 511116e6579f367b | # G2 implementation traceability | 1 | 42 | 55 | 0 |
| docs/gap-audit-2026-10-02.md | 637 | 988d4d87d59f3927 | # EOIP implementation gap audit & prioritized backlog | 25 | 168 | 31 | 0 |
| docs/graph-algorithms.md | 210 | 11eaaeba82fcd2a4 | # EOIP Graph Algorithms | 34 | 16 | 1 | 0 |
| docs/hubble-local.md | 224 | 2b4bb14ee5414b6c | # Hubble Basics + standalone RocksDB | 7 | 64 | 6 | 0 |
| docs/hubble-runtime-validation.md | 441 | 81ce2c1021bafe9b | # Hubble Runtime Validation Report | 15 | 73 | 24 | 0 |
| docs/ingestion.md | 239 | b0379195968be509 | # EOIP Ingestion Pipeline | 17 | 42 | 2 | 0 |
| docs/ontology.md | 249 | e8ecb9fd3244f1cc | # EOIP Ontology | 20 | 41 | 0 | 0 |
| docs/phase-completion-audit-2026-10-03.md | 400 | 1d800705701bf92f | # EOIP/KnowGridFlow — Phase Completion Audit Checklist | 8 | 126 | 31 | 0 |
| docs/query-engine.md | 220 | 8b9eb7c9596ae1a8 | # EOIP Query Engine | 14 | 13 | 3 | 0 |
| docs/rag.md | 196 | 3e2d4d4fdc38ad45 | # EOIP GraphRAG Retrieval System | 23 | 24 | 1 | 0 |
| docs/validation-evidence-phase1.md | 92 | 80072c222615f24c | # Audit phase 1: validation evidence foundation | 5 | 19 | 2 | 0 |
| EOIP-engg-doc-pkg/00-specification-audit-and-enhancements.md | 108 | 4084401be2f9b048 | # Specification Audit and Requirement Enhancements | 8 | 43 | 5 | 0 |
| EOIP-engg-doc-pkg/01-project-vision.md | 42 | a9f4126e7cda138e | # Project Vision | 5 | 12 | 2 | 0 |
| EOIP-engg-doc-pkg/02-scope-and-objectives.md | 42 | da8fc1ec0fa54030 | # Scope and Objectives | 5 | 13 | 2 | 0 |
| EOIP-engg-doc-pkg/03-functional-requirements.md | 683 | 64cb376f0dbe2231 | # Functional Requirements | 68 | 176 | 82 | 0 |
| EOIP-engg-doc-pkg/04-non-functional-requirements.md | 171 | 320a62c9ffdb4729 | # Non-Functional Requirements | 17 | 49 | 17 | 0 |
| EOIP-engg-doc-pkg/05-system-requirements.md | 42 | 4c873fc951d3b2b0 | # System Requirements | 5 | 10 | 2 | 0 |
| EOIP-engg-doc-pkg/06-architecture.md | 333 | 378ea79b522f93f1 | # Target Architecture | 26 | 98 | 11 | 0 |
| EOIP-engg-doc-pkg/07-component-architecture.md | 72 | d3a24cfb3b2ed58d | # Component Architecture | 6 | 30 | 4 | 0 |
| EOIP-engg-doc-pkg/08-deployment-architecture.md | 79 | 9d51ccb4232b1759 | # Deployment Architecture | 6 | 34 | 3 | 0 |
| EOIP-engg-doc-pkg/09-data-architecture.md | 44 | 61d1dcff86d4f1c9 | # Data Architecture | 5 | 14 | 3 | 0 |
| EOIP-engg-doc-pkg/10-enterprise-ontology.md | 40 | 575ab79dc9c8a8ce | # Enterprise Ontology | 5 | 12 | 2 | 0 |
| EOIP-engg-doc-pkg/11-graph-schema.md | 62 | fe22f215c4a66449 | # HugeGraph Graph Schema | 11 | 15 | 3 | 0 |
| EOIP-engg-doc-pkg/12-meta-graph-design.md | 40 | 6341b6e7c1b9ba8a | # Meta Graph Design | 5 | 14 | 2 | 0 |
| EOIP-engg-doc-pkg/13-relationship-model.md | 40 | 1f05151a7643b0be | # Relationship Model | 5 | 9 | 2 | 0 |
| EOIP-engg-doc-pkg/14-temporal-graph.md | 39 | f01e0612210929d5 | # Temporal Graph | 5 | 11 | 2 | 0 |
| EOIP-engg-doc-pkg/15-provenance-lineage.md | 40 | dab70baf28956a5c | # Provenance and Lineage | 5 | 11 | 2 | 0 |
| EOIP-engg-doc-pkg/16-identity-resolution.md | 39 | 830ae3dd340aa98b | # Identity Resolution | 5 | 8 | 2 | 0 |
| EOIP-engg-doc-pkg/17-code-graph.md | 42 | d91b112a87f4ba9b | # Code Graph | 5 | 12 | 2 | 0 |
| EOIP-engg-doc-pkg/18-ingestion-architecture.md | 53 | 3e93ca3b2205284a | # Ingestion Architecture | 5 | 15 | 2 | 0 |
| EOIP-engg-doc-pkg/19-connector-framework.md | 41 | b1e1d92bc0f14632 | # Connector Framework | 5 | 13 | 2 | 0 |
| EOIP-engg-doc-pkg/20-jira-connector-requirements.md | 39 | 03ece9c052dffe27 | # Jira Connector Requirements | 5 | 12 | 2 | 0 |
| EOIP-engg-doc-pkg/21-confluence-connector-requirements.md | 38 | 91eb356b39a6e57f | # Confluence Connector Requirements | 5 | 12 | 2 | 0 |
| EOIP-engg-doc-pkg/22-gitlab-connector-requirements.md | 40 | 97b43c085178485d | # Git/GitLab Connector Requirements | 5 | 12 | 2 | 0 |
| EOIP-engg-doc-pkg/23-servicenow-connector-requirements.md | 38 | fad7d4bb88d6979b | # ServiceNow Connector Requirements | 5 | 12 | 2 | 0 |
| EOIP-engg-doc-pkg/24-file-web-connectors.md | 42 | eb3eba2f719d6c98 | # File and Intranet Connector Requirements | 5 | 15 | 3 | 0 |
| EOIP-engg-doc-pkg/25-query-engine-requirements.md | 57 | d9d5bf16ceec79b4 | # Query Engine Requirements | 6 | 17 | 2 | 0 |
| EOIP-engg-doc-pkg/26-query-engine-implementation.md | 66 | 3a1c64f75138a2db | # Query Engine Implementation | 6 | 15 | 2 | 0 |
| EOIP-engg-doc-pkg/27-ontology-validation.md | 39 | 60d4bf8611772fde | # Ontology Validation | 5 | 13 | 2 | 0 |
| EOIP-engg-doc-pkg/28-graph-quality.md | 39 | fca6db75053af9c4 | # Graph Quality | 5 | 11 | 2 | 0 |
| EOIP-engg-doc-pkg/29-rag-architecture.md | 58 | 5e54064da716a275 | # RAG Architecture | 5 | 19 | 2 | 0 |
| EOIP-engg-doc-pkg/30-agent-architecture.md | 61 | c3ed1557a759f09a | # Agent Architecture | 5 | 21 | 4 | 0 |
| EOIP-engg-doc-pkg/31-multi-agent-architecture.md | 40 | eef840078cfd3b73 | # Multi-Agent Architecture | 5 | 13 | 3 | 0 |
| EOIP-engg-doc-pkg/32-memory-engineering.md | 39 | 88ecb00f48144b36 | # Memory Engineering | 5 | 11 | 3 | 0 |
| EOIP-engg-doc-pkg/33-context-engineering.md | 42 | c84989bb7e3d445e | # Context Engineering | 5 | 12 | 2 | 0 |
| EOIP-engg-doc-pkg/34-loop-engineering.md | 38 | 99365da1f8722607 | # Loop Engineering | 5 | 10 | 3 | 0 |
| EOIP-engg-doc-pkg/35-graph-engineering.md | 42 | 32bd915a1f0ecda5 | # Graph Engineering | 5 | 15 | 3 | 0 |
| EOIP-engg-doc-pkg/36-harness-engineering.md | 42 | 96bab7392e47c670 | # Harness Engineering | 5 | 12 | 4 | 0 |
| EOIP-engg-doc-pkg/37-graph-over-loop.md | 41 | d24e82f0ba204915 | # Graph-over-Loop Engineering | 5 | 14 | 3 | 0 |
| EOIP-engg-doc-pkg/38-loop-over-graph.md | 40 | 485afc1c22f72037 | # Loop-over-Graph Engineering | 5 | 12 | 2 | 0 |
| EOIP-engg-doc-pkg/39-mcp-architecture.md | 40 | 8b6b87c21af8527f | # MCP Architecture | 5 | 13 | 2 | 0 |
| EOIP-engg-doc-pkg/40-human-control-model.md | 39 | bded93a051cefc64 | # Human Control Model | 5 | 10 | 4 | 0 |
| EOIP-engg-doc-pkg/41-xai-explainability.md | 40 | 6ca04e7069563b68 | # XAI and Explainability | 5 | 11 | 2 | 0 |
| EOIP-engg-doc-pkg/42-web-user-ui-ux.md | 40 | e132992f6e40fc08 | # Web User UI/UX | 5 | 12 | 2 | 0 |
| EOIP-engg-doc-pkg/43-admin-ui-ux.md | 43 | 51418136f2da9db1 | # Admin UI/UX | 5 | 16 | 2 | 0 |
| EOIP-engg-doc-pkg/44-vscode-extension.md | 42 | 2fa124c6b2cbdf3d | # VS Code Extension | 5 | 12 | 2 | 0 |
| EOIP-engg-doc-pkg/45-api-specification.md | 43 | 0490c01bc97d2f6a | # API Specification | 5 | 14 | 2 | 0 |
| EOIP-engg-doc-pkg/46-security-architecture.md | 56 | ad4920a094b72336 | # Security Architecture | 6 | 19 | 3 | 0 |
| EOIP-engg-doc-pkg/47-threat-model.md | 49 | 99300cd99900462c | # Threat Model | 5 | 20 | 4 | 0 |
| EOIP-engg-doc-pkg/48-data-privacy.md | 40 | 0552010a6a511631 | # Data Privacy | 5 | 12 | 3 | 0 |
| EOIP-engg-doc-pkg/49-local-ai-model-strategy.md | 40 | de1cb70f9ff2fbd6 | # Local AI Model Strategy | 5 | 11 | 2 | 0 |
| EOIP-engg-doc-pkg/50-observability.md | 38 | 6970b55ea4e5c583 | # Observability | 5 | 10 | 2 | 0 |
| EOIP-engg-doc-pkg/51-performance.md | 45 | 5f805a1ef26d4601 | # Performance Engineering | 6 | 13 | 3 | 0 |
| EOIP-engg-doc-pkg/52-scalability.md | 40 | 78f1f8edf18cec3d | # Scalability | 5 | 10 | 2 | 0 |
| EOIP-engg-doc-pkg/53-backup-restore.md | 38 | 8f0c89d7fdae0847 | # Backup and Restore | 5 | 12 | 2 | 0 |
| EOIP-engg-doc-pkg/54-devsecops.md | 40 | 0b2828d21715beb0 | # DevSecOps | 5 | 8 | 3 | 0 |
| EOIP-engg-doc-pkg/55-testing-strategy.md | 110 | 8144dd3192640122 | # Testing Strategy | 3 | 58 | 2 | 0 |
| EOIP-engg-doc-pkg/56-rag-agent-evaluation.md | 42 | c1c60235456e071c | # RAG and Agent Evaluation | 5 | 14 | 4 | 0 |
| EOIP-engg-doc-pkg/57-graph-validation-test-plan.md | 43 | 56db120b4aa616ee | # Graph Validation Test Plan | 5 | 15 | 3 | 0 |
| EOIP-engg-doc-pkg/58-end-to-end-test-plan.md | 42 | b9455a372b8783b3 | # End-to-End Test Plan | 5 | 14 | 3 | 0 |
| EOIP-engg-doc-pkg/59-docker-deployment.md | 64 | eb03176662a12d24 | # Docker Deployment | 5 | 26 | 2 | 0 |
| EOIP-engg-doc-pkg/60-operational-runbook.md | 41 | ef9949f7fbdf855c | # Operational Runbook | 5 | 10 | 2 | 0 |
| EOIP-engg-doc-pkg/61-demo-playbook.md | 61 | ebaeaf581099c518 | # Demo Playbook | 5 | 15 | 2 | 0 |
| EOIP-engg-doc-pkg/62-risk-register.md | 27 | 03d8a989d2d5c6a0 | # Risk Register | 1 | 11 | 2 | 0 |
| EOIP-engg-doc-pkg/63-assumptions.md | 31 | 7aa01411ac203d6c | # Assumptions | 4 | 12 | 0 | 0 |
| EOIP-engg-doc-pkg/64-decisions-and-adrs.md | 39 | 56297c0d7fa2ad13 | # Architecture Decisions and ADRs | 11 | 11 | 1 | 0 |
| EOIP-engg-doc-pkg/65-glossary.md | 50 | adb5755791eb1298 | # Glossary | 3 | 15 | 3 | 0 |
| EOIP-engg-doc-pkg/66-phase-roadmap.md | 64 | 0abe43097d378431 | # Phased Roadmap | 11 | 19 | 0 | 0 |
| EOIP-engg-doc-pkg/67-implementation-plan.md | 265 | a1f98fb4bf0f5b95 | # Master Implementation Plan | 17 | 119 | 3 | 0 |
| EOIP-engg-doc-pkg/68-project-structure.md | 87 | 65a6a5522f63778f | # Project Structure | 5 | 27 | 3 | 0 |
| EOIP-engg-doc-pkg/69-dependency-license-sbom.md | 37 | 786168e188b0f10a | # Dependency, License and SBOM | 5 | 7 | 3 | 0 |
| EOIP-engg-doc-pkg/70-acceptance-criteria.md | 131 | 0e81f7132284033c | # Acceptance Criteria | 4 | 77 | 2 | 0 |
| EOIP-engg-doc-pkg/71-research-and-verification-basis.md | 31 | 566fe15c918c8ef0 | # Research and Verification Basis | 4 | 9 | 0 | 0 |
| EOIP-engg-doc-pkg/72-requirement-traceability.md | 128 | 0befd674dec4ccad | # Requirement Traceability Matrix | 2 | 90 | 0 | 0 |
| EOIP-engg-doc-pkg/73-architecture-diagrams.md | 293 | 093459aac532aaca | # Architecture Diagram Catalog | 18 | 77 | 3 | 0 |
| EOIP-engg-doc-pkg/74-data-contracts.md | 209 | c15dbe1425373dbc | # Data Contracts | 16 | 2 | 1 | 0 |
| EOIP-engg-doc-pkg/75-self-review-and-gap-closure.md | 40 | fef0185d9760b222 | # Architecture Self-Review and Gap Closure | 11 | 12 | 4 | 0 |
| EOIP-engg-doc-pkg/76-multi-backend.md | 179 | e81496b6a52ee043 | # EOIP Multi-Backend GraphStore | 15 | 25 | 0 | 0 |
| EOIP-engg-doc-pkg/diagrams/01-system-context.md | 18 | 6f847a1ba8b1d0aa | # 01-system-context | 1 | 11 | 0 | 0 |
| EOIP-engg-doc-pkg/diagrams/02-container-architecture.md | 24 | c31b925367eaf0ef | # 02-container-architecture | 1 | 14 | 0 | 0 |
| EOIP-engg-doc-pkg/diagrams/03-ingestion-pipeline.md | 10 | f5f4117822eb038b | # 03-ingestion-pipeline | 1 | 3 | 0 | 0 |
| EOIP-engg-doc-pkg/diagrams/04-enterprise-graph-architecture.md | 17 | 2d71f91e5ff70a90 | # 04-enterprise-graph-architecture | 1 | 3 | 0 | 0 |
| EOIP-engg-doc-pkg/diagrams/05-meta-graph.md | 14 | 909fc44ec2001519 | # 05-meta-graph | 1 | 2 | 0 | 0 |
| EOIP-engg-doc-pkg/diagrams/06-code-graph.md | 12 | d6034dd75433ab01 | # 06-code-graph | 1 | 2 | 0 | 0 |
| EOIP-engg-doc-pkg/diagrams/07-cross-domain-relationship-graph.md | 15 | 5cdc57d4e6d4a79f | # 07-cross-domain-relationship-graph | 1 | 1 | 0 | 0 |
| EOIP-engg-doc-pkg/diagrams/08-query-execution.md | 14 | ed8bfa064f74d3f9 | # 08-query-execution | 1 | 2 | 0 | 0 |
| EOIP-engg-doc-pkg/diagrams/09-graphrag.md | 14 | 0510787faaeba3f9 | # 09-graphrag | 1 | 1 | 0 | 0 |
| EOIP-engg-doc-pkg/diagrams/10-agent-runtime.md | 18 | 34383ce35fa2b472 | # 10-agent-runtime | 1 | 6 | 0 | 0 |
| EOIP-engg-doc-pkg/diagrams/11-multi-agent-orchestration.md | 17 | 1e88f82099e5e7da | # 11-multi-agent-orchestration | 1 | 1 | 0 | 0 |
| EOIP-engg-doc-pkg/diagrams/12-mcp-architecture.md | 12 | 7af6721c67e1ed4a | # 12-mcp-architecture | 1 | 3 | 0 | 0 |
| EOIP-engg-doc-pkg/diagrams/13-human-control-architecture.md | 13 | 62be85ba2c9a6bd6 | # 13-human-control-architecture | 1 | 4 | 3 | 0 |
| EOIP-engg-doc-pkg/diagrams/14-web-ui-architecture.md | 14 | f11f4edb2ed1f5df | # 14-web-ui-architecture | 1 | 9 | 0 | 0 |
| EOIP-engg-doc-pkg/diagrams/15-vscode-architecture.md | 12 | 51803364d8f3c76b | # 15-vscode-architecture | 1 | 5 | 0 | 0 |
| EOIP-engg-doc-pkg/diagrams/16-deployment.md | 21 | 8cf441ee2cbbe9e5 | # 16-deployment | 1 | 6 | 0 | 0 |
| EOIP-engg-doc-pkg/diagrams/17-mvp-e2e-flow.md | 22 | e5e469cde30763ee | # 17-mvp-e2e-flow | 1 | 3 | 0 | 0 |
| EOIP-engg-doc-pkg/DOCUMENTATION-INDEX.md | 101 | e492b6fae9836855 | # Documentation Index | 3 | 40 | 2 | 0 |
| EOIP-engg-doc-pkg/examples/demo_documentation.md | 3 | 66c5a2431dd62e82 | # EOIP-123 Impact Analysis | 1 | 0 | 0 | 0 |
| EOIP-engg-doc-pkg/gaps-implementation.md | 1216 | 48286e54a0776ce4 | # gaps-implementation.md | 155 | 183 | 65 | 0 |
| EOIP-engg-doc-pkg/gaps-requirements.md | 1401 | 76ed4843e3f32f69 | # gaps-requirements.md | 152 | 313 | 294 | 296 |
| EOIP-engg-doc-pkg/gaps2-implementation.md | 1625 | 610101b8885c55b8 | # gaps2-implementation.md | 337 | 155 | 3 | 0 |
| EOIP-engg-doc-pkg/gaps2-requirements.md | 2059 | dfb9b47bbf3cfb25 | # gaps2-requirements.md | 452 | 397 | 3 | 364 |
| EOIP-engg-doc-pkg/implementation/wp-agent-memory.md | 77 | 9f72fc15038d4cff | # WP-AGENT-MEMORY Implementation Plan | 9 | 42 | 2 | 0 |
| EOIP-engg-doc-pkg/implementation/wp-codegraph.md | 67 | 69f1742ee7be7eec | # WP-CODEGRAPH Implementation Plan | 8 | 24 | 2 | 0 |
| EOIP-engg-doc-pkg/implementation/wp-connectors.md | 107 | d088338c0da4e9e6 | # WP-CONNECTORS Implementation Plan | 12 | 59 | 0 | 0 |
| EOIP-engg-doc-pkg/implementation/wp-experience.md | 77 | 7387b1b6dbce48a2 | # WP-EXPERIENCE Implementation Plan | 9 | 44 | 0 | 0 |
| EOIP-engg-doc-pkg/implementation/wp-foundation.md | 67 | f3e58f7181d30a75 | # WP-FOUNDATION Implementation Plan | 8 | 30 | 0 | 0 |
| EOIP-engg-doc-pkg/implementation/wp-ingestion.md | 67 | 32732c84523978b4 | # WP-INGESTION Implementation Plan | 8 | 32 | 1 | 0 |
| EOIP-engg-doc-pkg/implementation/wp-mcp.md | 37 | 8c7ee26a187fc1be | # WP-MCP Implementation Plan | 5 | 20 | 0 | 0 |
| EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md | 137 | 05ccb1b4a514712c | # WP-ONTOLOGY-GRAPH Implementation Plan | 15 | 79 | 2 | 0 |
| EOIP-engg-doc-pkg/implementation/wp-query.md | 107 | 16ead715beffd155 | # WP-QUERY Implementation Plan | 12 | 46 | 1 | 0 |
| EOIP-engg-doc-pkg/implementation/wp-rag.md | 77 | 3d55d1cac4ad980d | # WP-RAG Implementation Plan | 9 | 45 | 0 | 0 |
| EOIP-engg-doc-pkg/implementation/wp-security-ops.md | 157 | 2ddae9a952d1bd7c | # WP-SECURITY-OPS Implementation Plan | 17 | 96 | 2 | 0 |
| EOIP-engg-doc-pkg/implementation/wp-validation.md | 47 | ed959d83ce6d3163 | # WP-VALIDATION Implementation Plan | 6 | 21 | 1 | 0 |
| EOIP-engg-doc-pkg/KGR-implementation-plan.md | 2838 | 863c5bac10c21f2d | # KGR — Knowledge Graph Renderer: Phase-by-Phase Implementation Plan | 192 | 409 | 72 | 0 |
| EOIP-engg-doc-pkg/KGR-requirements.md | 1145 | 923ea7e8acea158f | # KGR — Knowledge Graph Renderer & Explorer: Requirements Specification | 105 | 293 | 34 | 0 |
| EOIP-engg-doc-pkg/knowgridflow-product-architecture.md | 2010 | 40549755cc02fb22 | # KnowGridFlow Product Architecture | 142 | 334 | 14 | 0 |
| EOIP-engg-doc-pkg/MVP-implementation-plan.md | 590 | f47280f32166d976 | # MVP Implementation Plan | 40 | 204 | 4 | 0 |
| EOIP-engg-doc-pkg/MVP-requirements.md | 275 | 18ab7fb37df6b910 | # MVP Requirements | 37 | 147 | 1 | 0 |
| EOIP-engg-doc-pkg/README.md | 49 | fa49b45b12511926 | # Enterprise Ontology & Intelligence Platform (EOIP) — Engineering Documentation Package | 6 | 13 | 1 | 0 |
| examples/demo-enterprise/README.md | 28 | d0d1e3a5fe417883 | # Northstar enterprise demo pack | 3 | 7 | 1 | 0 |
| examples/demo-enterprise/wiki/checkout-latency-runbook.md | 12 | bd18c1105504516c | # Checkout latency incident runbook | 1 | 3 | 0 | 0 |
| examples/demo-enterprise/wiki/checkout-risk-architecture.md | 34 | d95bc157842bc188 | # Checkout risk architecture | 6 | 5 | 5 | 0 |
| examples/demo-repo/README.md | 4 | b23a7c8fb1478172 | # EOIP-1 requirement trace | 1 | 1 | 0 | 0 |
| handoff_template.md | 39 | 414c79298224ac20 | # EOIP Handoff Template | 1 | 3 | 2 | 0 |
| instruction.md | 140 | 60e70b0d3ede0845 | # EOIP Agent Orchestration Instructions and Contracts | 8 | 22 | 13 | 0 |
| memory.md | 326 | c3e3e53d2216bb17 | # EOIP Coordination Memory | 12 | 94 | 39 | 0 |
| onboarding_checklist.md | 27 | e471f62f5d43279c | # EOIP Onboarding Checklist | 1 | 3 | 1 | 0 |
| onboarding_prompts.md | 71 | 5683270bbb484534 | # EOIP Onboarding and Resume Prompts | 4 | 7 | 5 | 0 |
| README.md | 117 | de063f7145110438 | # EOIP — Enterprise Ontology & Intelligence Platform | 5 | 50 | 5 | 0 |
| roles.md | 526 | c28e5068f007c156 | # EOIP Application Roles, Activities and Persona Lines | 71 | 199 | 24 | 0 |
| secrets.example/README.md | 24 | a8feb4a87029e4fb | # Secrets Directory | 3 | 4 | 0 | 0 |
| tickets/requirements-map.md | 28 | b1298e7d2c2830f6 | # EOIP Requirements and Coordination Map | 2 | 8 | 5 | 0 |
| tickets/ticket-20261004-001.md | 83 | 2f7fca404abf1f6e | ## Reconciliation - 2026-10-04 | 2 | 14 | 2 | 0 |
| tickets/ticket-20261004-002.md | 61 | c678640944c63915 | (no markdown heading) | 0 | 5 | 4 | 0 |
| tickets/ticket-20261004-003.md | 110 | 21ad600d2671b653 | (no markdown heading) | 0 | 33 | 24 | 0 |
| tickets/ticket-20261004-004.md | 66 | 67ae81d49e282cdb | ## Verified gap and scope | 2 | 13 | 5 | 0 |
| tickets/ticket-20261004-005.md | 109 | b90cd30f943b1649 | (no markdown heading) | 0 | 35 | 2 | 0 |
| tickets/ticket-template.md | 38 | 01a97139f1c81bf2 | # EOIP Ticket Template | 1 | 4 | 6 | 0 |
| todo-status.md | 33 | 949d82469a6a472d | # EOIP Ticket Queue | 2 | 6 | 8 | 0 |

## Consolidated Product Requirements

The application to reconstruct is an Enterprise/Engineering Intelligence Platform that ingests heterogeneous enterprise sources, resolves identities and provenance, builds a temporal semantic graph, exposes query/RAG/agent/MCP/API/UI experiences, and can run locally in Docker while remaining portable across graph backends such as HugeGraph, Neptune, Neo4j, and memory for tests.

### Core Functional Requirement Groups

| ID | Group | Consolidated requirement |
| --- | --- | --- |
| FR-01 | Ingestion foundation | Connectors, source contracts, cursoring, baseline loads, incremental sync, retry/dead-letter handling, file parsing, web/API ingestion, and evidence preservation. |
| FR-02 | Ontology and graph | Enterprise ontology, schema generation, semantic validation, identity resolution, provenance, lineage, temporal graph, relationship model, graph quality, and graph algorithms. |
| FR-03 | Code and engineering intelligence | Repository/code graph extraction, commits, services, APIs, ownership, SBOM, CI/CD/runtime/observability evidence, architecture links, and engineering risk reasoning. |
| FR-04 | Query and retrieval | EOQL/query engine, graph traversal, evidence-backed GraphRAG, explainable retrieval, citations, ranking, filters, and consistent API/UI/MCP access. |
| FR-05 | Agentic operations | Tool registry, MCP governance, agent memory, human approval controls, audit trails, risk classification, and governed automation over graph-backed knowledge. |
| FR-06 | User experience | Web UI, admin UI, Hubble/local graph exploration, VS Code extension, demo walkthroughs, dashboards, source views, lineage views, and operational controls. |
| FR-07 | Deployment and operations | Docker local deployment, HA deployment path, backup/restore, observability, performance, security, privacy, DevSecOps, runbooks, validation evidence, and acceptance testing. |
| FR-08 | Product packaging | Documentation index, traceability, decisions/ADRs, assumptions, risk register, license/SBOM awareness, demo readiness, and reconstruction instructions. |

### Non-Functional Requirement Groups

| ID | Group | Consolidated requirement |
| --- | --- | --- |
| NFR-01 | Truth and traceability | Every answer, graph assertion, requirement, test, and audit claim must be traceable to source evidence or marked as inferred/unverified. |
| NFR-02 | Security and governance | Secrets, tokens, RBAC, destructive operations, audit logs, privacy controls, connector scopes, and deployment hardening must be explicit and testable. |
| NFR-03 | Portability | The graph persistence layer must preserve the EOIP graph contract while allowing client-selected graph systems through adapters and configuration. |
| NFR-04 | Reliability | Local Docker startup must complete with healthy services; ingestion must tolerate retries and partial source failures; backup/restore must be documented and verifiable. |
| NFR-05 | Performance and scale | Batch ingestion, traversal budgets, retrieval latency, indexing strategy, and benchmark evidence must be maintained as product acceptance criteria. |
| NFR-06 | Usability | MVP workflows must be directly usable without relying on marketing pages or unsupported manual steps. |

## Supplied Audit Requirements

The following table is the merged machine-readable requirement set from `.tmp/gap-coverage-audit.json` and `.tmp/g2-coverage-audit.json`. These rows are preserved so the reconstruction can map back to the generated gap gates.

| Audit | Requirement ID | Priority | Status | Phase | Section | Source | Title | Implementation refs | Test refs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| g2-coverage-audit.json | G2-ARCHC-001 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 13. Architecture Conformance & Semantic Architecture Compiler | EOIP-engg-doc-pkg/gaps2-requirements.md:1107 | G2-ARCHC-001 | packages/eoip/gaps/g2_readiness.py:9, packages/eoip/gaps/g2_readiness.py:224, packages/eoip/graph/conformance.py:1 | tests/unit/test_g2_readiness.py:6 |
| g2-coverage-audit.json | G2-ARCHC-002 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 13. Architecture Conformance & Semantic Architecture Compiler | EOIP-engg-doc-pkg/gaps2-requirements.md:1113 | G2-ARCHC-002 | packages/eoip/gaps/g2_readiness.py:9, packages/eoip/gaps/g2_readiness.py:224, packages/eoip/graph/conformance.py:1 | tests/unit/test_g2_readiness.py:6 |
| g2-coverage-audit.json | G2-ARCHC-003 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 13. Architecture Conformance & Semantic Architecture Compiler | EOIP-engg-doc-pkg/gaps2-requirements.md:1116 | G2-ARCHC-003 | packages/eoip/gaps/g2_readiness.py:9, packages/eoip/gaps/g2_readiness.py:224, packages/eoip/graph/conformance.py:1 | tests/unit/test_g2_readiness.py:6 |
| g2-coverage-audit.json | G2-ARCHC-004 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 13. Architecture Conformance & Semantic Architecture Compiler | EOIP-engg-doc-pkg/gaps2-requirements.md:1123 | G2-ARCHC-004 | packages/eoip/gaps/g2_readiness.py:9, packages/eoip/gaps/g2_readiness.py:224, packages/eoip/graph/conformance.py:1 | tests/unit/test_g2_readiness.py:6 |
| g2-coverage-audit.json | G2-ARCHC-005 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 13. Architecture Conformance & Semantic Architecture Compiler | EOIP-engg-doc-pkg/gaps2-requirements.md:1126 | G2-ARCHC-005 | packages/eoip/gaps/g2_readiness.py:9, packages/eoip/gaps/g2_readiness.py:224, packages/eoip/graph/conformance.py:1 | tests/unit/test_g2_readiness.py:6 |
| g2-coverage-audit.json | G2-ARCHC-006 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 13. Architecture Conformance & Semantic Architecture Compiler | EOIP-engg-doc-pkg/gaps2-requirements.md:1129 | G2-ARCHC-006 | packages/eoip/gaps/g2_readiness.py:9, packages/eoip/gaps/g2_readiness.py:224, packages/eoip/graph/conformance.py:1 | tests/unit/test_g2_readiness.py:6 |
| g2-coverage-audit.json | G2-ARCHC-007 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 13. Architecture Conformance & Semantic Architecture Compiler | EOIP-engg-doc-pkg/gaps2-requirements.md:1132 | G2-ARCHC-007 | packages/eoip/gaps/g2_readiness.py:9, packages/eoip/gaps/g2_readiness.py:224, packages/eoip/graph/conformance.py:1 | tests/unit/test_g2_readiness.py:6 |
| g2-coverage-audit.json | G2-ARCHC-008 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 13. Architecture Conformance & Semantic Architecture Compiler | EOIP-engg-doc-pkg/gaps2-requirements.md:1135 | G2-ARCHC-008 | packages/eoip/gaps/g2_readiness.py:9, packages/eoip/gaps/g2_readiness.py:224, packages/eoip/graph/conformance.py:1 | tests/unit/test_g2_readiness.py:6 |
| g2-coverage-audit.json | G2-ARCHC-009 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 13. Architecture Conformance & Semantic Architecture Compiler | EOIP-engg-doc-pkg/gaps2-requirements.md:1138 | G2-ARCHC-009 | packages/eoip/gaps/g2_readiness.py:9, packages/eoip/gaps/g2_readiness.py:224, packages/eoip/graph/conformance.py:1 | tests/unit/test_g2_readiness.py:6 |
| g2-coverage-audit.json | G2-KD-001 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 21. Knowledge Debt | EOIP-engg-doc-pkg/gaps2-requirements.md:1368 | G2-KD-001 | packages/eoip/gaps/g2_readiness.py:26, packages/eoip/gaps/g2_readiness.py:193, packages/eoip/graph/knowledge_debt.py:1 | tests/unit/test_g2_readiness.py:23 |
| g2-coverage-audit.json | G2-KD-002 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 21. Knowledge Debt | EOIP-engg-doc-pkg/gaps2-requirements.md:1371 | G2-KD-002 | packages/eoip/gaps/g2_readiness.py:26, packages/eoip/gaps/g2_readiness.py:193, packages/eoip/graph/knowledge_debt.py:1 | tests/unit/test_g2_readiness.py:23 |
| g2-coverage-audit.json | G2-KD-003 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 21. Knowledge Debt | EOIP-engg-doc-pkg/gaps2-requirements.md:1386 | G2-KD-003 | packages/eoip/gaps/g2_readiness.py:26, packages/eoip/gaps/g2_readiness.py:193, packages/eoip/graph/knowledge_debt.py:1 | tests/unit/test_g2_readiness.py:23 |
| g2-coverage-audit.json | G2-KD-004 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 21. Knowledge Debt | EOIP-engg-doc-pkg/gaps2-requirements.md:1395 | G2-KD-004 | packages/eoip/gaps/g2_readiness.py:26, packages/eoip/gaps/g2_readiness.py:193, packages/eoip/graph/knowledge_debt.py:1 | tests/unit/test_g2_readiness.py:23 |
| g2-coverage-audit.json | G2-KD-005 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 21. Knowledge Debt | EOIP-engg-doc-pkg/gaps2-requirements.md:1398 | G2-KD-005 | packages/eoip/gaps/g2_readiness.py:26, packages/eoip/gaps/g2_readiness.py:193, packages/eoip/graph/knowledge_debt.py:1 | tests/unit/test_g2_readiness.py:23 |
| g2-coverage-audit.json | G2-KD-006 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 21. Knowledge Debt | EOIP-engg-doc-pkg/gaps2-requirements.md:1401 | G2-KD-006 | packages/eoip/gaps/g2_readiness.py:26, packages/eoip/gaps/g2_readiness.py:193, packages/eoip/graph/knowledge_debt.py:1 | tests/unit/test_g2_readiness.py:23 |
| g2-coverage-audit.json | G2-PM-001 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 17. Process Mining | EOIP-engg-doc-pkg/gaps2-requirements.md:1251 | G2-PM-001 | packages/eoip/gaps/g2_readiness.py:30, packages/eoip/gaps/g2_readiness.py:228, packages/eoip/graph/process_mining.py:1 | tests/unit/test_g2_readiness.py:27 |
| g2-coverage-audit.json | G2-PM-002 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 17. Process Mining | EOIP-engg-doc-pkg/gaps2-requirements.md:1254 | G2-PM-002 | packages/eoip/gaps/g2_readiness.py:30, packages/eoip/gaps/g2_readiness.py:228, packages/eoip/graph/process_mining.py:1 | tests/unit/test_g2_readiness.py:27 |
| g2-coverage-audit.json | G2-PM-003 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 17. Process Mining | EOIP-engg-doc-pkg/gaps2-requirements.md:1257 | G2-PM-003 | packages/eoip/gaps/g2_readiness.py:30, packages/eoip/gaps/g2_readiness.py:228, packages/eoip/graph/process_mining.py:1 | tests/unit/test_g2_readiness.py:27 |
| g2-coverage-audit.json | G2-PM-004 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 17. Process Mining | EOIP-engg-doc-pkg/gaps2-requirements.md:1266 | G2-PM-004 | packages/eoip/gaps/g2_readiness.py:30, packages/eoip/gaps/g2_readiness.py:228, packages/eoip/graph/process_mining.py:1 | tests/unit/test_g2_readiness.py:27 |
| g2-coverage-audit.json | G2-PM-005 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 17. Process Mining | EOIP-engg-doc-pkg/gaps2-requirements.md:1269 | G2-PM-005 | packages/eoip/gaps/g2_readiness.py:30, packages/eoip/gaps/g2_readiness.py:228, packages/eoip/graph/process_mining.py:1 | tests/unit/test_g2_readiness.py:27 |
| g2-coverage-audit.json | G2-QOP-001 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 19. Native Semantic Query Operators | EOIP-engg-doc-pkg/gaps2-requirements.md:1317 | G2-QOP-001 — WHY | packages/eoip/gaps/g2_readiness.py:31, packages/eoip/gaps/g2_readiness.py:192, packages/eoip/graph/query_operators.py:1 | tests/unit/test_g2_readiness.py:28 |
| g2-coverage-audit.json | G2-QOP-002 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 19. Native Semantic Query Operators | EOIP-engg-doc-pkg/gaps2-requirements.md:1320 | G2-QOP-002 — WHY NOT | packages/eoip/gaps/g2_readiness.py:31, packages/eoip/gaps/g2_readiness.py:192, packages/eoip/graph/query_operators.py:1 | tests/unit/test_g2_readiness.py:28 |
| g2-coverage-audit.json | G2-QOP-003 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 19. Native Semantic Query Operators | EOIP-engg-doc-pkg/gaps2-requirements.md:1323 | G2-QOP-003 — WHAT IF | packages/eoip/gaps/g2_readiness.py:31, packages/eoip/gaps/g2_readiness.py:192, packages/eoip/graph/query_operators.py:1 | tests/unit/test_g2_readiness.py:28, tests/unit/test_gap_coverage.py:111 |
| g2-coverage-audit.json | G2-QOP-004 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 19. Native Semantic Query Operators | EOIP-engg-doc-pkg/gaps2-requirements.md:1326 | G2-QOP-004 — WHAT CHANGED | packages/eoip/gaps/g2_readiness.py:31, packages/eoip/gaps/g2_readiness.py:192, packages/eoip/graph/query_operators.py:1 | tests/unit/test_g2_readiness.py:28 |
| g2-coverage-audit.json | G2-QOP-005 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 19. Native Semantic Query Operators | EOIP-engg-doc-pkg/gaps2-requirements.md:1329 | G2-QOP-005 — WHEN | packages/eoip/gaps/g2_readiness.py:31, packages/eoip/gaps/g2_readiness.py:192, packages/eoip/graph/query_operators.py:1 | tests/unit/test_g2_readiness.py:28 |
| g2-coverage-audit.json | G2-QOP-006 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 19. Native Semantic Query Operators | EOIP-engg-doc-pkg/gaps2-requirements.md:1332 | G2-QOP-006 — WHO | packages/eoip/gaps/g2_readiness.py:31, packages/eoip/gaps/g2_readiness.py:192, packages/eoip/graph/query_operators.py:1 | tests/unit/test_g2_readiness.py:28 |
| g2-coverage-audit.json | G2-QOP-007 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 19. Native Semantic Query Operators | EOIP-engg-doc-pkg/gaps2-requirements.md:1335 | G2-QOP-007 — WHERE | packages/eoip/gaps/g2_readiness.py:31, packages/eoip/gaps/g2_readiness.py:192, packages/eoip/graph/query_operators.py:1 | tests/unit/test_g2_readiness.py:28 |
| g2-coverage-audit.json | G2-QOP-008 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 19. Native Semantic Query Operators | EOIP-engg-doc-pkg/gaps2-requirements.md:1338 | G2-QOP-008 — HOW | packages/eoip/gaps/g2_readiness.py:31, packages/eoip/gaps/g2_readiness.py:192, packages/eoip/graph/query_operators.py:1 | tests/unit/test_g2_readiness.py:28 |
| g2-coverage-audit.json | G2-QOP-009 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 19. Native Semantic Query Operators | EOIP-engg-doc-pkg/gaps2-requirements.md:1341 | G2-QOP-009 | packages/eoip/gaps/g2_readiness.py:31, packages/eoip/gaps/g2_readiness.py:192, packages/eoip/graph/query_operators.py:1 | tests/unit/test_g2_readiness.py:28 |
| g2-coverage-audit.json | G2-SLO-001 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 22. Knowledge Reliability SLOs | EOIP-engg-doc-pkg/gaps2-requirements.md:1408 | G2-SLO-001 | packages/eoip/gaps/g2_readiness.py:35, packages/eoip/gaps/g2_readiness.py:194, packages/eoip/graph/knowledge_debt.py:1 | tests/unit/test_g2_readiness.py:32 |
| g2-coverage-audit.json | G2-SLO-002 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 22. Knowledge Reliability SLOs | EOIP-engg-doc-pkg/gaps2-requirements.md:1418 | G2-SLO-002 | packages/eoip/gaps/g2_readiness.py:35, packages/eoip/gaps/g2_readiness.py:194, packages/eoip/graph/knowledge_debt.py:1 | tests/unit/test_g2_readiness.py:32 |
| g2-coverage-audit.json | G2-SLO-003 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 22. Knowledge Reliability SLOs | EOIP-engg-doc-pkg/gaps2-requirements.md:1421 | G2-SLO-003 | packages/eoip/gaps/g2_readiness.py:35, packages/eoip/gaps/g2_readiness.py:194, packages/eoip/graph/knowledge_debt.py:1 | tests/unit/test_g2_readiness.py:32 |
| g2-coverage-audit.json | G2-SLO-004 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 22. Knowledge Reliability SLOs | EOIP-engg-doc-pkg/gaps2-requirements.md:1424 | G2-SLO-004 | packages/eoip/gaps/g2_readiness.py:35, packages/eoip/gaps/g2_readiness.py:194, packages/eoip/graph/knowledge_debt.py:1 | tests/unit/test_g2_readiness.py:32 |
| g2-coverage-audit.json | G2-SLO-005 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 22. Knowledge Reliability SLOs | EOIP-engg-doc-pkg/gaps2-requirements.md:1427 | G2-SLO-005 | packages/eoip/gaps/g2_readiness.py:35, packages/eoip/gaps/g2_readiness.py:194, packages/eoip/graph/knowledge_debt.py:1 | tests/unit/test_g2_readiness.py:32 |
| g2-coverage-audit.json | G2-TIME-001 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 11. Enterprise Time Machine | EOIP-engg-doc-pkg/gaps2-requirements.md:1042 | G2-TIME-001 | packages/eoip/gaps/g2_readiness.py:54, packages/eoip/gaps/g2_readiness.py:191 | tests/unit/test_g2_readiness.py:51 |
| g2-coverage-audit.json | G2-TIME-002 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 11. Enterprise Time Machine | EOIP-engg-doc-pkg/gaps2-requirements.md:1045 | G2-TIME-002 | packages/eoip/gaps/g2_readiness.py:54, packages/eoip/gaps/g2_readiness.py:191 | tests/unit/test_g2_readiness.py:51 |
| g2-coverage-audit.json | G2-TIME-003 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 11. Enterprise Time Machine | EOIP-engg-doc-pkg/gaps2-requirements.md:1048 | G2-TIME-003 | packages/eoip/gaps/g2_readiness.py:54, packages/eoip/gaps/g2_readiness.py:191 | tests/unit/test_g2_readiness.py:51 |
| g2-coverage-audit.json | G2-TIME-004 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 11. Enterprise Time Machine | EOIP-engg-doc-pkg/gaps2-requirements.md:1051 | G2-TIME-004 | packages/eoip/gaps/g2_readiness.py:54, packages/eoip/gaps/g2_readiness.py:191 | tests/unit/test_g2_readiness.py:51 |
| g2-coverage-audit.json | G2-TIME-005 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 11. Enterprise Time Machine | EOIP-engg-doc-pkg/gaps2-requirements.md:1054 | G2-TIME-005 | packages/eoip/gaps/g2_readiness.py:54, packages/eoip/gaps/g2_readiness.py:191 | tests/unit/test_g2_readiness.py:51 |
| g2-coverage-audit.json | G2-TIME-006 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 11. Enterprise Time Machine | EOIP-engg-doc-pkg/gaps2-requirements.md:1057 | G2-TIME-006 | packages/eoip/gaps/g2_readiness.py:54, packages/eoip/gaps/g2_readiness.py:191 | tests/unit/test_g2_readiness.py:51 |
| g2-coverage-audit.json | G2-TIME-007 | P2 | done | 10. G2-P7 — Temporal, Architecture & Process Intelligence | 11. Enterprise Time Machine | EOIP-engg-doc-pkg/gaps2-requirements.md:1060 | G2-TIME-007 | packages/eoip/gaps/g2_readiness.py:54, packages/eoip/gaps/g2_readiness.py:191 | tests/unit/test_g2_readiness.py:51 |
| gap-coverage-audit.json | GAP-HA-001 | P1 | done | 10. Phase 7 — Enterprise Security, HA & Operational Maturity | 4. Competitive Study / 4.9 Amazon Neptune / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:322 | GAP-HA-001: Provide self-managed HA patterns for HugeGraph distributed mode | packages/eoip/ha.py:1, packages/eoip/ha.py:32, deploy/docker-compose.ha.yml:89 | tests/unit/test_ha_lease.py:1, tests/unit/test_ha_lease.py:7 |
| gap-coverage-audit.json | GAP-LITE-001 | P2 | done | 10. Phase 7 — Enterprise Security, HA & Operational Maturity | 4. Competitive Study / 4.6 Cambridge Semantics Anzo / Graph Studio / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:253 | GAP-LITE-001: Support laptop/dev, single-server production and distributed production profiles | packages/eoip/future_scope.py:17, packages/eoip/future_scope.py:48, packages/eoip/future_scope.py:396 | tests/unit/test_enterprise_gap_completion.py:34 |
| gap-coverage-audit.json | GAP-LITE-002 | P2 | done | 10. Phase 7 — Enterprise Security, HA & Operational Maturity | 4. Competitive Study / 4.6 Cambridge Semantics Anzo / Graph Studio / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:254 | GAP-LITE-002: Implement automated sizing and capacity planning | packages/eoip/future_scope.py:17, packages/eoip/future_scope.py:49, packages/eoip/future_scope.py:396 | tests/unit/test_enterprise_gap_completion.py:34 |
| g2-coverage-audit.json | G2-CAP-001 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 18. Knowledge Capsules | EOIP-engg-doc-pkg/gaps2-requirements.md:1278 | G2-CAP-001 | packages/eoip/gaps/g2_readiness.py:10, packages/eoip/gaps/g2_readiness.py:229, packages/eoip/graph/capsules.py:1 | tests/unit/test_capsules.py:1, tests/unit/test_g2_readiness.py:7 |
| g2-coverage-audit.json | G2-CAP-002 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 18. Knowledge Capsules | EOIP-engg-doc-pkg/gaps2-requirements.md:1289 | G2-CAP-002 | packages/eoip/gaps/g2_readiness.py:10, packages/eoip/gaps/g2_readiness.py:229, packages/eoip/graph/capsules.py:1 | tests/unit/test_capsules.py:1, tests/unit/test_g2_readiness.py:7 |
| g2-coverage-audit.json | G2-CAP-003 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 18. Knowledge Capsules | EOIP-engg-doc-pkg/gaps2-requirements.md:1292 | G2-CAP-003 | packages/eoip/gaps/g2_readiness.py:10, packages/eoip/gaps/g2_readiness.py:229, packages/eoip/graph/capsules.py:1 | tests/unit/test_capsules.py:1, tests/unit/test_g2_readiness.py:7 |
| g2-coverage-audit.json | G2-CAP-004 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 18. Knowledge Capsules | EOIP-engg-doc-pkg/gaps2-requirements.md:1295 | G2-CAP-004 | packages/eoip/gaps/g2_readiness.py:10, packages/eoip/gaps/g2_readiness.py:229, packages/eoip/graph/capsules.py:1 | tests/unit/test_capsules.py:1, tests/unit/test_g2_readiness.py:7 |
| g2-coverage-audit.json | G2-CAP-005 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 18. Knowledge Capsules | EOIP-engg-doc-pkg/gaps2-requirements.md:1298 | G2-CAP-005 | packages/eoip/gaps/g2_readiness.py:10, packages/eoip/gaps/g2_readiness.py:229, packages/eoip/graph/capsules.py:1 | tests/unit/test_capsules.py:1, tests/unit/test_g2_readiness.py:7 |
| g2-coverage-audit.json | G2-CAP-006 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 18. Knowledge Capsules | EOIP-engg-doc-pkg/gaps2-requirements.md:1308 | G2-CAP-006 | packages/eoip/gaps/g2_readiness.py:10, packages/eoip/gaps/g2_readiness.py:229, packages/eoip/graph/capsules.py:1 | tests/unit/test_capsules.py:1, tests/unit/test_g2_readiness.py:7 |
| g2-coverage-audit.json | G2-IMMUNE-001 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 15. Enterprise Knowledge Immune System | EOIP-engg-doc-pkg/gaps2-requirements.md:1180 | G2-IMMUNE-001 | packages/eoip/gaps/g2_readiness.py:24, packages/eoip/gaps/g2_readiness.py:226 | tests/unit/test_g2_readiness.py:21 |
| g2-coverage-audit.json | G2-IMMUNE-002 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 15. Enterprise Knowledge Immune System | EOIP-engg-doc-pkg/gaps2-requirements.md:1183 | G2-IMMUNE-002 | packages/eoip/gaps/g2_readiness.py:24, packages/eoip/gaps/g2_readiness.py:226 | tests/unit/test_g2_readiness.py:21 |
| g2-coverage-audit.json | G2-IMMUNE-003 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 15. Enterprise Knowledge Immune System | EOIP-engg-doc-pkg/gaps2-requirements.md:1186 | G2-IMMUNE-003 | packages/eoip/gaps/g2_readiness.py:24, packages/eoip/gaps/g2_readiness.py:226 | tests/unit/test_g2_readiness.py:21 |
| g2-coverage-audit.json | G2-IMMUNE-004 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 15. Enterprise Knowledge Immune System | EOIP-engg-doc-pkg/gaps2-requirements.md:1189 | G2-IMMUNE-004 | packages/eoip/gaps/g2_readiness.py:24, packages/eoip/gaps/g2_readiness.py:226 | tests/unit/test_g2_readiness.py:21 |
| g2-coverage-audit.json | G2-IMMUNE-005 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 15. Enterprise Knowledge Immune System | EOIP-engg-doc-pkg/gaps2-requirements.md:1192 | G2-IMMUNE-005 | packages/eoip/gaps/g2_readiness.py:24, packages/eoip/gaps/g2_readiness.py:226 | tests/unit/test_g2_readiness.py:21 |
| g2-coverage-audit.json | G2-IMMUNE-006 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 15. Enterprise Knowledge Immune System | EOIP-engg-doc-pkg/gaps2-requirements.md:1195 | G2-IMMUNE-006 | packages/eoip/gaps/g2_readiness.py:24, packages/eoip/gaps/g2_readiness.py:226 | tests/unit/test_g2_readiness.py:21 |
| g2-coverage-audit.json | G2-IMMUNE-007 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 15. Enterprise Knowledge Immune System | EOIP-engg-doc-pkg/gaps2-requirements.md:1198 | G2-IMMUNE-007 | packages/eoip/gaps/g2_readiness.py:24, packages/eoip/gaps/g2_readiness.py:226 | tests/unit/test_g2_readiness.py:21 |
| g2-coverage-audit.json | G2-IMMUNE-008 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 15. Enterprise Knowledge Immune System | EOIP-engg-doc-pkg/gaps2-requirements.md:1201 | G2-IMMUNE-008 | packages/eoip/gaps/g2_readiness.py:24, packages/eoip/gaps/g2_readiness.py:226 | tests/unit/test_g2_readiness.py:21 |
| g2-coverage-audit.json | G2-IMMUNE-009 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 15. Enterprise Knowledge Immune System | EOIP-engg-doc-pkg/gaps2-requirements.md:1204 | G2-IMMUNE-009 | packages/eoip/gaps/g2_readiness.py:24, packages/eoip/gaps/g2_readiness.py:226 | tests/unit/test_g2_readiness.py:21 |
| g2-coverage-audit.json | G2-IMMUNE-010 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 15. Enterprise Knowledge Immune System | EOIP-engg-doc-pkg/gaps2-requirements.md:1207 | G2-IMMUNE-010 | packages/eoip/gaps/g2_readiness.py:24, packages/eoip/gaps/g2_readiness.py:226 | tests/unit/test_g2_readiness.py:21 |
| g2-coverage-audit.json | G2-IMMUNE-011 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 15. Enterprise Knowledge Immune System | EOIP-engg-doc-pkg/gaps2-requirements.md:1210 | G2-IMMUNE-011 | packages/eoip/gaps/g2_readiness.py:24, packages/eoip/gaps/g2_readiness.py:226 | tests/unit/test_g2_readiness.py:21 |
| g2-coverage-audit.json | G2-IMMUNE-012 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 15. Enterprise Knowledge Immune System | EOIP-engg-doc-pkg/gaps2-requirements.md:1213 | G2-IMMUNE-012 | packages/eoip/gaps/g2_readiness.py:24, packages/eoip/gaps/g2_readiness.py:226 | tests/unit/test_g2_readiness.py:21 |
| g2-coverage-audit.json | G2-IMMUNE-013 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 15. Enterprise Knowledge Immune System | EOIP-engg-doc-pkg/gaps2-requirements.md:1216 | G2-IMMUNE-013 | packages/eoip/gaps/g2_readiness.py:24, packages/eoip/gaps/g2_readiness.py:226 | tests/unit/test_g2_readiness.py:21 |
| g2-coverage-audit.json | G2-OEVO-001 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 16. Controlled Ontology Evolution | EOIP-engg-doc-pkg/gaps2-requirements.md:1223 | G2-OEVO-001 | packages/eoip/gaps/g2_readiness.py:28, packages/eoip/gaps/g2_readiness.py:227, packages/eoip/ontology/drift.py:1 | tests/unit/test_g2_readiness.py:25, tests/unit/test_ontology_drift_review.py:1 |
| g2-coverage-audit.json | G2-OEVO-002 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 16. Controlled Ontology Evolution | EOIP-engg-doc-pkg/gaps2-requirements.md:1226 | G2-OEVO-002 | packages/eoip/gaps/g2_readiness.py:28, packages/eoip/gaps/g2_readiness.py:227, packages/eoip/ontology/drift.py:1 | tests/unit/test_g2_readiness.py:25, tests/unit/test_ontology_drift_review.py:1 |
| g2-coverage-audit.json | G2-OEVO-003 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 16. Controlled Ontology Evolution | EOIP-engg-doc-pkg/gaps2-requirements.md:1229 | G2-OEVO-003 | packages/eoip/gaps/g2_readiness.py:28, packages/eoip/gaps/g2_readiness.py:227, packages/eoip/ontology/drift.py:1 | tests/unit/test_g2_readiness.py:25, tests/unit/test_ontology_drift_review.py:1 |
| g2-coverage-audit.json | G2-OEVO-004 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 16. Controlled Ontology Evolution | EOIP-engg-doc-pkg/gaps2-requirements.md:1238 | G2-OEVO-004 | packages/eoip/gaps/g2_readiness.py:28, packages/eoip/gaps/g2_readiness.py:227, packages/eoip/ontology/drift.py:1 | tests/unit/test_g2_readiness.py:25, tests/unit/test_ontology_drift_review.py:1 |
| g2-coverage-audit.json | G2-OEVO-005 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 16. Controlled Ontology Evolution | EOIP-engg-doc-pkg/gaps2-requirements.md:1241 | G2-OEVO-005 | packages/eoip/gaps/g2_readiness.py:28, packages/eoip/gaps/g2_readiness.py:227, packages/eoip/ontology/drift.py:1 | tests/unit/test_g2_readiness.py:25, tests/unit/test_ontology_drift_review.py:1 |
| g2-coverage-audit.json | G2-OEVO-006 | P2 | done | 11. G2-P8 — Knowledge Health & Governed AI | 16. Controlled Ontology Evolution | EOIP-engg-doc-pkg/gaps2-requirements.md:1244 | G2-OEVO-006 | packages/eoip/gaps/g2_readiness.py:28, packages/eoip/gaps/g2_readiness.py:227, packages/eoip/ontology/drift.py:1 | tests/unit/test_g2_readiness.py:25, tests/unit/test_ontology_drift_review.py:1 |
| gap-coverage-audit.json | GAP-GDS-001 | P1 | done | 11. Phase 8 — Advanced Analytics, Simulation & Predictive Intelligence | 4. Competitive Study / 4.2 Neo4j / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:144 | GAP-GDS-001: Create a local graph-analytics service with pluggable algorithms without requiring the authoritative graph to be copied permanently into another da | packages/eoip/gaps/enterprise_completion.py:29 | tests/unit/test_enterprise_gap_completion.py:22 |
| gap-coverage-audit.json | GAP-GDS-002 | P1 | done | 11. Phase 8 — Advanced Analytics, Simulation & Predictive Intelligence | 4. Competitive Study / 4.2 Neo4j / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:145 | GAP-GDS-002: Provide algorithms for PageRank, centrality, connected components, community detection, similarity, shortest path and dependency risk | packages/eoip/gaps/enterprise_completion.py:29 | tests/unit/test_enterprise_gap_completion.py:22 |
| g2-coverage-audit.json | G2-CAUSE-001 | P2 | done | 12. G2-P9 — Counterfactual Twin & Causal Intelligence | 14. Causal Intelligence | EOIP-engg-doc-pkg/gaps2-requirements.md:1147 | G2-CAUSE-001 | packages/eoip/gaps/g2_readiness.py:11, packages/eoip/gaps/g2_readiness.py:225, packages/eoip/graph/causal.py:1 | tests/unit/test_g2_readiness.py:8 |
| g2-coverage-audit.json | G2-CAUSE-002 | P2 | done | 12. G2-P9 — Counterfactual Twin & Causal Intelligence | 14. Causal Intelligence | EOIP-engg-doc-pkg/gaps2-requirements.md:1150 | G2-CAUSE-002 | packages/eoip/gaps/g2_readiness.py:11, packages/eoip/gaps/g2_readiness.py:225, packages/eoip/graph/causal.py:1 | tests/unit/test_g2_readiness.py:8 |
| g2-coverage-audit.json | G2-CAUSE-003 | P2 | done | 12. G2-P9 — Counterfactual Twin & Causal Intelligence | 14. Causal Intelligence | EOIP-engg-doc-pkg/gaps2-requirements.md:1157 | G2-CAUSE-003 | packages/eoip/gaps/g2_readiness.py:11, packages/eoip/gaps/g2_readiness.py:225, packages/eoip/graph/causal.py:1 | tests/unit/test_g2_readiness.py:8 |
| g2-coverage-audit.json | G2-CAUSE-004 | P2 | done | 12. G2-P9 — Counterfactual Twin & Causal Intelligence | 14. Causal Intelligence | EOIP-engg-doc-pkg/gaps2-requirements.md:1160 | G2-CAUSE-004 | packages/eoip/gaps/g2_readiness.py:11, packages/eoip/gaps/g2_readiness.py:225, packages/eoip/graph/causal.py:1 | tests/unit/test_g2_readiness.py:8 |
| g2-coverage-audit.json | G2-CAUSE-005 | P2 | done | 12. G2-P9 — Counterfactual Twin & Causal Intelligence | 14. Causal Intelligence | EOIP-engg-doc-pkg/gaps2-requirements.md:1168 | G2-CAUSE-005 | packages/eoip/gaps/g2_readiness.py:11, packages/eoip/gaps/g2_readiness.py:225, packages/eoip/graph/causal.py:1 | tests/unit/test_g2_readiness.py:8 |
| g2-coverage-audit.json | G2-CAUSE-006 | P2 | done | 12. G2-P9 — Counterfactual Twin & Causal Intelligence | 14. Causal Intelligence | EOIP-engg-doc-pkg/gaps2-requirements.md:1171 | G2-CAUSE-006 | packages/eoip/gaps/g2_readiness.py:11, packages/eoip/gaps/g2_readiness.py:225, packages/eoip/graph/causal.py:1 | tests/unit/test_g2_readiness.py:8 |
| g2-coverage-audit.json | G2-SIM-001 | P2 | done | 12. G2-P9 — Counterfactual Twin & Causal Intelligence | 12. Counterfactual Enterprise Twin / What-If Simulation | EOIP-engg-doc-pkg/gaps2-requirements.md:1067 | G2-SIM-001 | packages/eoip/gaps/g2_readiness.py:34, packages/eoip/gaps/g2_readiness.py:223, packages/eoip/graph/simulation.py:256 | tests/unit/test_g2_readiness.py:31 |
| g2-coverage-audit.json | G2-SIM-002 | P2 | done | 12. G2-P9 — Counterfactual Twin & Causal Intelligence | 12. Counterfactual Enterprise Twin / What-If Simulation | EOIP-engg-doc-pkg/gaps2-requirements.md:1070 | G2-SIM-002 | packages/eoip/gaps/g2_readiness.py:34, packages/eoip/gaps/g2_readiness.py:223, packages/eoip/graph/simulation.py:256 | tests/unit/test_g2_readiness.py:31 |
| g2-coverage-audit.json | G2-SIM-003 | P2 | done | 12. G2-P9 — Counterfactual Twin & Causal Intelligence | 12. Counterfactual Enterprise Twin / What-If Simulation | EOIP-engg-doc-pkg/gaps2-requirements.md:1073 | G2-SIM-003 | packages/eoip/gaps/g2_readiness.py:34, packages/eoip/gaps/g2_readiness.py:223, packages/eoip/graph/simulation.py:256 | tests/unit/test_g2_readiness.py:31 |
| g2-coverage-audit.json | G2-SIM-004 | P2 | done | 12. G2-P9 — Counterfactual Twin & Causal Intelligence | 12. Counterfactual Enterprise Twin / What-If Simulation | EOIP-engg-doc-pkg/gaps2-requirements.md:1083 | G2-SIM-004 | packages/eoip/gaps/g2_readiness.py:34, packages/eoip/gaps/g2_readiness.py:223, packages/eoip/graph/simulation.py:256 | tests/unit/test_g2_readiness.py:31 |
| g2-coverage-audit.json | G2-SIM-005 | P2 | done | 12. G2-P9 — Counterfactual Twin & Causal Intelligence | 12. Counterfactual Enterprise Twin / What-If Simulation | EOIP-engg-doc-pkg/gaps2-requirements.md:1091 | G2-SIM-005 | packages/eoip/gaps/g2_readiness.py:34, packages/eoip/gaps/g2_readiness.py:223, packages/eoip/graph/simulation.py:256 | tests/unit/test_g2_readiness.py:31 |
| g2-coverage-audit.json | G2-SIM-006 | P2 | done | 12. G2-P9 — Counterfactual Twin & Causal Intelligence | 12. Counterfactual Enterprise Twin / What-If Simulation | EOIP-engg-doc-pkg/gaps2-requirements.md:1094 | G2-SIM-006 | packages/eoip/gaps/g2_readiness.py:34, packages/eoip/gaps/g2_readiness.py:223, packages/eoip/graph/simulation.py:256 | tests/unit/test_g2_readiness.py:31 |
| g2-coverage-audit.json | G2-SIM-007 | P2 | done | 12. G2-P9 — Counterfactual Twin & Causal Intelligence | 12. Counterfactual Enterprise Twin / What-If Simulation | EOIP-engg-doc-pkg/gaps2-requirements.md:1097 | G2-SIM-007 | packages/eoip/gaps/g2_readiness.py:34, packages/eoip/gaps/g2_readiness.py:223, packages/eoip/graph/simulation.py:256 | tests/unit/test_g2_readiness.py:31 |
| gap-coverage-audit.json | GAP-APP-001 | P2 | done | 12. Phase 9 — Ecosystem, Extensions & Domain Packs | 4. Competitive Study / 4.7 metaphactory / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:273 | GAP-APP-001: Build a Knowledge App Builder that can compose query, table, graph, timeline, KPI and evidence panels from saved semantic queries | packages/eoip/future_scope.py:19, packages/eoip/future_scope.py:52, packages/eoip/future_scope.py:461 | tests/unit/test_enterprise_gap_completion.py:8 |
| gap-coverage-audit.json | GAP-APP-002 | P2 | done | 12. Phase 9 — Ecosystem, Extensions & Domain Packs | 4. Competitive Study / 4.7 metaphactory / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:274 | GAP-APP-002: App definitions must be configuration-as-code and exportable | packages/eoip/future_scope.py:19, packages/eoip/future_scope.py:53, packages/eoip/future_scope.py:461 | tests/unit/test_enterprise_gap_completion.py:8 |
| gap-coverage-audit.json | GAP-EXT-001 | P2 | done | 12. Phase 9 — Ecosystem, Extensions & Domain Packs | 4. Competitive Study / 4.7 metaphactory / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:276 | GAP-EXT-001: Support extension SDKs rather than requiring modification of the core platform | packages/eoip/marketplace/signing.py:1, packages/eoip/marketplace/__init__.py:1 | tests/unit/test_marketplace.py:1 |
| gap-coverage-audit.json | GAP-MKT-001 | P2 | done | 12. Phase 9 — Ecosystem, Extensions & Domain Packs | 36. Schema & Mapping Marketplace / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:915 | GAP-MKT-001: Package reusable ontology modules | packages/eoip/marketplace/manifest.py:1, packages/eoip/marketplace/__init__.py:1, apps/api/extended.py:201 | tests/unit/test_marketplace.py:1 |
| gap-coverage-audit.json | GAP-MKT-002 | P2 | done | 12. Phase 9 — Ecosystem, Extensions & Domain Packs | 36. Schema & Mapping Marketplace / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:916 | GAP-MKT-002: Package connector mappings | packages/eoip/marketplace/manifest.py:1, packages/eoip/marketplace/__init__.py:1, apps/api/extended.py:201 | tests/unit/test_marketplace.py:1 |
| gap-coverage-audit.json | GAP-MKT-003 | P2 | done | 12. Phase 9 — Ecosystem, Extensions & Domain Packs | 36. Schema & Mapping Marketplace / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:917 | GAP-MKT-003: Package query templates | packages/eoip/marketplace/packager.py:1, packages/eoip/marketplace/sample.py:1, packages/eoip/marketplace/__init__.py:1 | tests/unit/test_marketplace.py:1 |
| gap-coverage-audit.json | GAP-MKT-004 | P2 | done | 12. Phase 9 — Ecosystem, Extensions & Domain Packs | 36. Schema & Mapping Marketplace / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:918 | GAP-MKT-004: Package validation rules | packages/eoip/marketplace/installer.py:1, packages/eoip/marketplace/installer.py:21, packages/eoip/marketplace/manifest.py:33 | tests/unit/test_marketplace.py:1 |
| gap-coverage-audit.json | GAP-MKT-005 | P2 | done | 12. Phase 9 — Ecosystem, Extensions & Domain Packs | 36. Schema & Mapping Marketplace / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:919 | GAP-MKT-005: Package agent workflows | packages/eoip/marketplace/installer.py:1, packages/eoip/marketplace/installer.py:85, packages/eoip/marketplace/packager.py:1 | tests/unit/test_marketplace.py:1 |
| gap-coverage-audit.json | GAP-MKT-006 | P2 | done | 12. Phase 9 — Ecosystem, Extensions & Domain Packs | 36. Schema & Mapping Marketplace / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:920 | GAP-MKT-006: Package dashboards | packages/eoip/marketplace/installer.py:1, packages/eoip/marketplace/installer.py:85, packages/eoip/marketplace/registry.py:1 | tests/unit/test_marketplace.py:1 |
| gap-coverage-audit.json | GAP-MKT-007 | P2 | done | 12. Phase 9 — Ecosystem, Extensions & Domain Packs | 36. Schema & Mapping Marketplace / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:921 | GAP-MKT-007: Dependency/version management | packages/eoip/marketplace/installer.py:25, packages/eoip/marketplace/installer.py:85, packages/eoip/marketplace/signing.py:1 | tests/unit/test_marketplace.py:1 |
| gap-coverage-audit.json | GAP-MKT-008 | P2 | done | 12. Phase 9 — Ecosystem, Extensions & Domain Packs | 36. Schema & Mapping Marketplace / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:922 | GAP-MKT-008: Signed packages in later phases | packages/eoip/marketplace/registry.py:1, packages/eoip/marketplace/registry.py:40, packages/eoip/marketplace/registry.py:101 | tests/unit/test_marketplace.py:1 |
| gap-coverage-audit.json | GAP-TEMPLATE-001 | P2 | done | 12. Phase 9 — Ecosystem, Extensions & Domain Packs | 4. Competitive Study / 4.7 metaphactory / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:275 | GAP-TEMPLATE-001: Provide packaged templates for engineering, audit, risk, incident, architecture and compliance use cases | packages/eoip/future_scope.py:19, packages/eoip/future_scope.py:54, packages/eoip/future_scope.py:481 | tests/unit/test_enterprise_gap_completion.py:47 |
| g2-coverage-audit.json | G2-ADMIN-001 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 26. Admin / Engineering GUI Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1551 | G2-ADMIN-001 | packages/eoip/gaps/g2_readiness.py:7, packages/eoip/gaps/g2_readiness.py:258, apps/web/src/admin/index.jsx:8 | tests/unit/test_g2_readiness.py:4 |
| g2-coverage-audit.json | G2-ADMIN-002 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 26. Admin / Engineering GUI Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1554 | G2-ADMIN-002 | packages/eoip/gaps/g2_readiness.py:7, packages/eoip/gaps/g2_readiness.py:258, apps/web/src/admin/index.jsx:9 | tests/unit/test_g2_readiness.py:4 |
| g2-coverage-audit.json | G2-ADMIN-003 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 26. Admin / Engineering GUI Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1557 | G2-ADMIN-003 | packages/eoip/gaps/g2_readiness.py:7, packages/eoip/gaps/g2_readiness.py:258, apps/web/src/admin/index.jsx:10 | tests/unit/test_g2_readiness.py:4 |
| g2-coverage-audit.json | G2-ADMIN-004 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 26. Admin / Engineering GUI Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1560 | G2-ADMIN-004 | packages/eoip/gaps/g2_readiness.py:7, packages/eoip/gaps/g2_readiness.py:258 | tests/unit/test_g2_readiness.py:4 |
| g2-coverage-audit.json | G2-ADMIN-005 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 26. Admin / Engineering GUI Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1563 | G2-ADMIN-005 | packages/eoip/gaps/g2_readiness.py:7, packages/eoip/gaps/g2_readiness.py:258 | tests/unit/test_g2_readiness.py:4 |
| g2-coverage-audit.json | G2-ADMIN-006 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 26. Admin / Engineering GUI Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1566 | G2-ADMIN-006 | packages/eoip/gaps/g2_readiness.py:7, packages/eoip/gaps/g2_readiness.py:258 | tests/unit/test_g2_readiness.py:4 |
| g2-coverage-audit.json | G2-ADMIN-007 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 26. Admin / Engineering GUI Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1569 | G2-ADMIN-007 | packages/eoip/gaps/g2_readiness.py:7, packages/eoip/gaps/g2_readiness.py:258 | tests/unit/test_g2_readiness.py:4 |
| g2-coverage-audit.json | G2-ADMIN-008 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 26. Admin / Engineering GUI Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1572 | G2-ADMIN-008 | packages/eoip/gaps/g2_readiness.py:7, packages/eoip/gaps/g2_readiness.py:258 | tests/unit/test_g2_readiness.py:4 |
| g2-coverage-audit.json | G2-ADMIN-009 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 26. Admin / Engineering GUI Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1575 | G2-ADMIN-009 | packages/eoip/gaps/g2_readiness.py:7, packages/eoip/gaps/g2_readiness.py:258 | tests/unit/test_g2_readiness.py:4 |
| g2-coverage-audit.json | G2-ADMIN-010 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 26. Admin / Engineering GUI Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1578 | G2-ADMIN-010 | packages/eoip/gaps/g2_readiness.py:7, packages/eoip/gaps/g2_readiness.py:258 | tests/unit/test_g2_readiness.py:4 |
| g2-coverage-audit.json | G2-ADMIN-011 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 26. Admin / Engineering GUI Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1581 | G2-ADMIN-011 | packages/eoip/gaps/g2_readiness.py:7, packages/eoip/gaps/g2_readiness.py:258 | tests/unit/test_g2_readiness.py:4 |
| g2-coverage-audit.json | G2-ADMIN-012 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 26. Admin / Engineering GUI Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1584 | G2-ADMIN-012 | packages/eoip/gaps/g2_readiness.py:7, packages/eoip/gaps/g2_readiness.py:258 | tests/unit/test_g2_readiness.py:4 |
| g2-coverage-audit.json | G2-ADMIN-013 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 26. Admin / Engineering GUI Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1587 | G2-ADMIN-013 | packages/eoip/gaps/g2_readiness.py:7, packages/eoip/gaps/g2_readiness.py:258 | tests/unit/test_g2_readiness.py:4 |
| g2-coverage-audit.json | G2-ADMIN-014 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 26. Admin / Engineering GUI Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1590 | G2-ADMIN-014 | packages/eoip/gaps/g2_readiness.py:7, packages/eoip/gaps/g2_readiness.py:258 | tests/unit/test_g2_readiness.py:4 |
| g2-coverage-audit.json | G2-ADMIN-015 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 26. Admin / Engineering GUI Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1593 | G2-ADMIN-015 | packages/eoip/gaps/g2_readiness.py:7, packages/eoip/gaps/g2_readiness.py:258 | tests/unit/test_g2_readiness.py:4 |
| g2-coverage-audit.json | G2-ADMIN-016 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 26. Admin / Engineering GUI Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1596 | G2-ADMIN-016 | packages/eoip/gaps/g2_readiness.py:7, packages/eoip/gaps/g2_readiness.py:258 | tests/unit/test_g2_readiness.py:4 |
| g2-coverage-audit.json | G2-ADMIN-017 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 26. Admin / Engineering GUI Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1599 | G2-ADMIN-017 | packages/eoip/gaps/g2_readiness.py:7, packages/eoip/gaps/g2_readiness.py:258 | tests/unit/test_g2_readiness.py:4, tests/unit/test_g2_readiness.py:100 |
| g2-coverage-audit.json | G2-UX-GRAPH-001 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 24. Advanced Graph Canvas | EOIP-engg-doc-pkg/gaps2-requirements.md:1474 | G2-UX-GRAPH-001 | packages/eoip/gaps/g2_readiness.py:56, packages/eoip/gaps/g2_readiness.py:256 | tests/unit/test_g2_readiness.py:53 |
| g2-coverage-audit.json | G2-UX-GRAPH-002 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 24. Advanced Graph Canvas | EOIP-engg-doc-pkg/gaps2-requirements.md:1477 | G2-UX-GRAPH-002 | packages/eoip/gaps/g2_readiness.py:56, packages/eoip/gaps/g2_readiness.py:256 | tests/unit/test_g2_readiness.py:53 |
| g2-coverage-audit.json | G2-UX-GRAPH-003 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 24. Advanced Graph Canvas | EOIP-engg-doc-pkg/gaps2-requirements.md:1480 | G2-UX-GRAPH-003 | packages/eoip/gaps/g2_readiness.py:56, packages/eoip/gaps/g2_readiness.py:256 | tests/unit/test_g2_readiness.py:53 |
| g2-coverage-audit.json | G2-UX-GRAPH-004 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 24. Advanced Graph Canvas | EOIP-engg-doc-pkg/gaps2-requirements.md:1483 | G2-UX-GRAPH-004 | packages/eoip/gaps/g2_readiness.py:56, packages/eoip/gaps/g2_readiness.py:256 | tests/unit/test_g2_readiness.py:53 |
| g2-coverage-audit.json | G2-UX-GRAPH-005 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 24. Advanced Graph Canvas | EOIP-engg-doc-pkg/gaps2-requirements.md:1486 | G2-UX-GRAPH-005 | packages/eoip/gaps/g2_readiness.py:56, packages/eoip/gaps/g2_readiness.py:256 | tests/unit/test_g2_readiness.py:53 |
| g2-coverage-audit.json | G2-UX-GRAPH-006 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 24. Advanced Graph Canvas | EOIP-engg-doc-pkg/gaps2-requirements.md:1489 | G2-UX-GRAPH-006 | packages/eoip/gaps/g2_readiness.py:56, packages/eoip/gaps/g2_readiness.py:256 | tests/unit/test_g2_readiness.py:53 |
| g2-coverage-audit.json | G2-UX-GRAPH-007 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 24. Advanced Graph Canvas | EOIP-engg-doc-pkg/gaps2-requirements.md:1492 | G2-UX-GRAPH-007 | packages/eoip/gaps/g2_readiness.py:56, packages/eoip/gaps/g2_readiness.py:256 | tests/unit/test_g2_readiness.py:53 |
| g2-coverage-audit.json | G2-UX-GRAPH-008 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 24. Advanced Graph Canvas | EOIP-engg-doc-pkg/gaps2-requirements.md:1495 | G2-UX-GRAPH-008 | packages/eoip/gaps/g2_readiness.py:56, packages/eoip/gaps/g2_readiness.py:256 | tests/unit/test_g2_readiness.py:53 |
| g2-coverage-audit.json | G2-UX-GRAPH-009 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 24. Advanced Graph Canvas | EOIP-engg-doc-pkg/gaps2-requirements.md:1498 | G2-UX-GRAPH-009 | packages/eoip/gaps/g2_readiness.py:56, packages/eoip/gaps/g2_readiness.py:256 | tests/unit/test_g2_readiness.py:53 |
| g2-coverage-audit.json | G2-UX-GRAPH-010 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 24. Advanced Graph Canvas | EOIP-engg-doc-pkg/gaps2-requirements.md:1501 | G2-UX-GRAPH-010 | packages/eoip/gaps/g2_readiness.py:56, packages/eoip/gaps/g2_readiness.py:256 | tests/unit/test_g2_readiness.py:53 |
| g2-coverage-audit.json | G2-UX-GRAPH-011 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 24. Advanced Graph Canvas | EOIP-engg-doc-pkg/gaps2-requirements.md:1504 | G2-UX-GRAPH-011 | packages/eoip/gaps/g2_readiness.py:56, packages/eoip/gaps/g2_readiness.py:256 | tests/unit/test_g2_readiness.py:53 |
| g2-coverage-audit.json | G2-UX-GRAPH-012 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 24. Advanced Graph Canvas | EOIP-engg-doc-pkg/gaps2-requirements.md:1507 | G2-UX-GRAPH-012 | packages/eoip/gaps/g2_readiness.py:56, packages/eoip/gaps/g2_readiness.py:256 | tests/unit/test_g2_readiness.py:53 |
| g2-coverage-audit.json | G2-UX-GRAPH-013 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 24. Advanced Graph Canvas | EOIP-engg-doc-pkg/gaps2-requirements.md:1510 | G2-UX-GRAPH-013 | packages/eoip/gaps/g2_readiness.py:56, packages/eoip/gaps/g2_readiness.py:256 | tests/unit/test_g2_readiness.py:53 |
| g2-coverage-audit.json | G2-UX-GRAPH-014 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 24. Advanced Graph Canvas | EOIP-engg-doc-pkg/gaps2-requirements.md:1513 | G2-UX-GRAPH-014 | packages/eoip/gaps/g2_readiness.py:56, packages/eoip/gaps/g2_readiness.py:256 | tests/unit/test_g2_readiness.py:53 |
| g2-coverage-audit.json | G2-UX-GRAPH-015 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 24. Advanced Graph Canvas | EOIP-engg-doc-pkg/gaps2-requirements.md:1516 | G2-UX-GRAPH-015 | packages/eoip/gaps/g2_readiness.py:56, packages/eoip/gaps/g2_readiness.py:256 | tests/unit/test_g2_readiness.py:53 |
| g2-coverage-audit.json | G2-UX-GRAPH-016 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 24. Advanced Graph Canvas | EOIP-engg-doc-pkg/gaps2-requirements.md:1519 | G2-UX-GRAPH-016 | packages/eoip/gaps/g2_readiness.py:56, packages/eoip/gaps/g2_readiness.py:256 | tests/unit/test_g2_readiness.py:53, tests/unit/test_gap_coverage.py:66 |
| g2-coverage-audit.json | G2-UX-LENS-001 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 23. Next-Generation GUI / Application Requirements / 23.1 Lens framework | EOIP-engg-doc-pkg/gaps2-requirements.md:1438 | G2-UX-LENS-001 | packages/eoip/gaps/g2_readiness.py:57, packages/eoip/gaps/g2_readiness.py:255, packages/eoip/graph/lens.py:1 | tests/unit/test_g2_readiness.py:54 |
| g2-coverage-audit.json | G2-UX-LENS-002 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 23. Next-Generation GUI / Application Requirements / 23.1 Lens framework | EOIP-engg-doc-pkg/gaps2-requirements.md:1464 | G2-UX-LENS-002 | packages/eoip/gaps/g2_readiness.py:57, packages/eoip/gaps/g2_readiness.py:255, packages/eoip/graph/lens.py:1 | tests/unit/test_g2_readiness.py:54 |
| g2-coverage-audit.json | G2-UX-LENS-003 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 23. Next-Generation GUI / Application Requirements / 23.1 Lens framework | EOIP-engg-doc-pkg/gaps2-requirements.md:1467 | G2-UX-LENS-003 | packages/eoip/gaps/g2_readiness.py:57, packages/eoip/gaps/g2_readiness.py:255, packages/eoip/graph/lens.py:1 | tests/unit/test_g2_readiness.py:54 |
| g2-coverage-audit.json | G2-UX-PLAY-001 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 25. Graph Playback | EOIP-engg-doc-pkg/gaps2-requirements.md:1526 | G2-UX-PLAY-001 | packages/eoip/gaps/g2_readiness.py:58, packages/eoip/gaps/g2_readiness.py:257 | tests/unit/test_g2_readiness.py:55 |
| g2-coverage-audit.json | G2-UX-PLAY-002 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 25. Graph Playback | EOIP-engg-doc-pkg/gaps2-requirements.md:1529 | G2-UX-PLAY-002 | packages/eoip/gaps/g2_readiness.py:58, packages/eoip/gaps/g2_readiness.py:257 | tests/unit/test_g2_readiness.py:55 |
| g2-coverage-audit.json | G2-UX-PLAY-003 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 25. Graph Playback | EOIP-engg-doc-pkg/gaps2-requirements.md:1538 | G2-UX-PLAY-003 | packages/eoip/gaps/g2_readiness.py:58, packages/eoip/gaps/g2_readiness.py:257 | tests/unit/test_g2_readiness.py:55 |
| g2-coverage-audit.json | G2-UX-PLAY-004 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 25. Graph Playback | EOIP-engg-doc-pkg/gaps2-requirements.md:1541 | G2-UX-PLAY-004 | packages/eoip/gaps/g2_readiness.py:58, packages/eoip/gaps/g2_readiness.py:257 | tests/unit/test_g2_readiness.py:55 |
| g2-coverage-audit.json | G2-UX-PLAY-005 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 25. Graph Playback | EOIP-engg-doc-pkg/gaps2-requirements.md:1544 | G2-UX-PLAY-005 | packages/eoip/gaps/g2_readiness.py:58, packages/eoip/gaps/g2_readiness.py:257 | tests/unit/test_g2_readiness.py:55 |
| g2-coverage-audit.json | G2-VSC-001 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 27. VS Code Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1606 | G2-VSC-001 | packages/eoip/gaps/g2_readiness.py:59, packages/eoip/gaps/g2_readiness.py:259 | tests/unit/test_g2_readiness.py:56 |
| g2-coverage-audit.json | G2-VSC-002 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 27. VS Code Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1609 | G2-VSC-002 | packages/eoip/gaps/g2_readiness.py:59, packages/eoip/gaps/g2_readiness.py:259 | tests/unit/test_g2_readiness.py:56 |
| g2-coverage-audit.json | G2-VSC-003 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 27. VS Code Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1612 | G2-VSC-003 | packages/eoip/gaps/g2_readiness.py:59, packages/eoip/gaps/g2_readiness.py:259 | tests/unit/test_g2_readiness.py:56 |
| g2-coverage-audit.json | G2-VSC-004 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 27. VS Code Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1615 | G2-VSC-004 | packages/eoip/gaps/g2_readiness.py:59, packages/eoip/gaps/g2_readiness.py:259 | tests/unit/test_g2_readiness.py:56 |
| g2-coverage-audit.json | G2-VSC-005 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 27. VS Code Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1618 | G2-VSC-005 | packages/eoip/gaps/g2_readiness.py:59, packages/eoip/gaps/g2_readiness.py:259 | tests/unit/test_g2_readiness.py:56 |
| g2-coverage-audit.json | G2-VSC-006 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 27. VS Code Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1621 | G2-VSC-006 | packages/eoip/gaps/g2_readiness.py:59, packages/eoip/gaps/g2_readiness.py:259 | tests/unit/test_g2_readiness.py:56 |
| g2-coverage-audit.json | G2-VSC-007 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 27. VS Code Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1624 | G2-VSC-007 | packages/eoip/gaps/g2_readiness.py:59, packages/eoip/gaps/g2_readiness.py:259 | tests/unit/test_g2_readiness.py:56 |
| g2-coverage-audit.json | G2-VSC-008 | P2 | done | 13. G2-P10 — Diamond-Standard UX & Production Hardening | 27. VS Code Additions | EOIP-engg-doc-pkg/gaps2-requirements.md:1627 | G2-VSC-008 | packages/eoip/gaps/g2_readiness.py:59, packages/eoip/gaps/g2_readiness.py:259 | tests/unit/test_g2_readiness.py:56 |
| g2-coverage-audit.json | G2-ARCH-001 | P0 | done | 3. G2-P0 — Contract & Architecture Alignment | 2. Non-Negotiable Architectural Principles | EOIP-engg-doc-pkg/gaps2-requirements.md:52 | G2-ARCH-001 — One acquisition contract | packages/eoip/gaps/g2_architecture.py:3, packages/eoip/gaps/g2_architecture.py:71, packages/eoip/gaps/g2_readiness.py:8 | tests/unit/test_g2_readiness.py:5, tests/unit/test_gap_coverage.py:8, tests/unit/test_gap_coverage.py:64 |
| g2-coverage-audit.json | G2-ARCH-002 | P0 | done | 3. G2-P0 — Contract & Architecture Alignment | 2. Non-Negotiable Architectural Principles | EOIP-engg-doc-pkg/gaps2-requirements.md:56 | G2-ARCH-002 — API/event first | packages/eoip/gaps/g2_architecture.py:3, packages/eoip/gaps/g2_architecture.py:72, packages/eoip/gaps/g2_readiness.py:8 | tests/unit/test_g2_readiness.py:5, tests/unit/test_gap_coverage.py:8 |
| g2-coverage-audit.json | G2-ARCH-003 | P0 | done | 3. G2-P0 — Contract & Architecture Alignment | 2. Non-Negotiable Architectural Principles | EOIP-engg-doc-pkg/gaps2-requirements.md:68 | G2-ARCH-003 — Deterministic first | packages/eoip/gaps/g2_architecture.py:3, packages/eoip/gaps/g2_architecture.py:73, packages/eoip/gaps/g2_readiness.py:8 | tests/unit/test_g2_readiness.py:5, tests/unit/test_gap_coverage.py:8 |
| g2-coverage-audit.json | G2-ARCH-004 | P0 | done | 3. G2-P0 — Contract & Architecture Alignment | 2. Non-Negotiable Architectural Principles | EOIP-engg-doc-pkg/gaps2-requirements.md:72 | G2-ARCH-004 — Preserve source fidelity | packages/eoip/gaps/g2_architecture.py:3, packages/eoip/gaps/g2_architecture.py:74, packages/eoip/gaps/g2_readiness.py:8 | tests/unit/test_g2_readiness.py:5, tests/unit/test_gap_coverage.py:8 |
| g2-coverage-audit.json | G2-ARCH-005 | P0 | done | 3. G2-P0 — Contract & Architecture Alignment | 2. Non-Negotiable Architectural Principles | EOIP-engg-doc-pkg/gaps2-requirements.md:76 | G2-ARCH-005 — HugeGraph is semantic operational truth | packages/eoip/gaps/g2_architecture.py:3, packages/eoip/gaps/g2_architecture.py:75, packages/eoip/gaps/g2_readiness.py:8 | tests/unit/test_g2_readiness.py:5, tests/unit/test_gap_coverage.py:8 |
| g2-coverage-audit.json | G2-ARCH-006 | P0 | done | 3. G2-P0 — Contract & Architecture Alignment | 2. Non-Negotiable Architectural Principles | EOIP-engg-doc-pkg/gaps2-requirements.md:80 | G2-ARCH-006 — No raw telemetry lake in HugeGraph | packages/eoip/gaps/g2_architecture.py:3, packages/eoip/gaps/g2_architecture.py:76, packages/eoip/gaps/g2_readiness.py:8 | tests/unit/test_g2_readiness.py:5, tests/unit/test_gap_coverage.py:8, tests/unit/test_gap_coverage.py:128 |
| g2-coverage-audit.json | G2-ARCH-007 | P0 | done | 3. G2-P0 — Contract & Architecture Alignment | 2. Non-Negotiable Architectural Principles | EOIP-engg-doc-pkg/gaps2-requirements.md:84 | G2-ARCH-007 — No destructive history overwrite | packages/eoip/gaps/g2_architecture.py:3, packages/eoip/gaps/g2_architecture.py:77, packages/eoip/gaps/g2_readiness.py:8 | tests/unit/test_confluence_body.py:138, tests/unit/test_confluence_metadata.py:92, tests/unit/test_g2_readiness.py:5 |
| g2-coverage-audit.json | G2-ARCH-008 | P0 | done | 3. G2-P0 — Contract & Architecture Alignment | 2. Non-Negotiable Architectural Principles | EOIP-engg-doc-pkg/gaps2-requirements.md:88 | G2-ARCH-008 — Current and historical views | packages/eoip/gaps/g2_architecture.py:3, packages/eoip/gaps/g2_architecture.py:78, packages/eoip/gaps/g2_readiness.py:8 | tests/unit/test_g2_readiness.py:5, tests/unit/test_gap_coverage.py:8 |
| g2-coverage-audit.json | G2-ARCH-009 | P0 | done | 3. G2-P0 — Contract & Architecture Alignment | 2. Non-Negotiable Architectural Principles | EOIP-engg-doc-pkg/gaps2-requirements.md:92 | G2-ARCH-009 — One semantic identity system | packages/eoip/gaps/g2_architecture.py:3, packages/eoip/gaps/g2_architecture.py:79, packages/eoip/gaps/g2_readiness.py:8 | tests/unit/test_g2_readiness.py:5, tests/unit/test_gap_coverage.py:8 |
| g2-coverage-audit.json | G2-ARCH-010 | P0 | done | 3. G2-P0 — Contract & Architecture Alignment | 2. Non-Negotiable Architectural Principles | EOIP-engg-doc-pkg/gaps2-requirements.md:96 | G2-ARCH-010 — Evidence is mandatory | packages/eoip/gaps/g2_architecture.py:3, packages/eoip/gaps/g2_architecture.py:80, packages/eoip/gaps/g2_readiness.py:8 | tests/unit/test_g2_readiness.py:5, tests/unit/test_gap_coverage.py:8, tests/unit/test_gap_coverage.py:123 |
| g2-coverage-audit.json | G2-ARCH-011 | P0 | done | 3. G2-P0 — Contract & Architecture Alignment | 2. Non-Negotiable Architectural Principles | EOIP-engg-doc-pkg/gaps2-requirements.md:100 | G2-ARCH-011 — AI is not the source of truth | packages/eoip/gaps/g2_architecture.py:3, packages/eoip/gaps/g2_architecture.py:81, packages/eoip/gaps/g2_readiness.py:8 | tests/unit/test_g2_readiness.py:5, tests/unit/test_gap_coverage.py:8, tests/unit/test_gap_coverage.py:128 |
| g2-coverage-audit.json | G2-ARCH-012 | P0 | done | 3. G2-P0 — Contract & Architecture Alignment | 2. Non-Negotiable Architectural Principles | EOIP-engg-doc-pkg/gaps2-requirements.md:104 | G2-ARCH-012 — Incremental by default after baseline | packages/eoip/gaps/g2_architecture.py:3, packages/eoip/gaps/g2_architecture.py:82, packages/eoip/gaps/g2_readiness.py:8 | tests/unit/test_g2_readiness.py:5, tests/unit/test_gap_coverage.py:8 |
| g2-coverage-audit.json | G2-ARCH-013 | P0 | done | 3. G2-P0 — Contract & Architecture Alignment | 2. Non-Negotiable Architectural Principles | EOIP-engg-doc-pkg/gaps2-requirements.md:108 | G2-ARCH-013 — Replayability | packages/eoip/gaps/g2_architecture.py:3, packages/eoip/gaps/g2_architecture.py:83, packages/eoip/gaps/g2_readiness.py:8 | tests/unit/test_g2_readiness.py:5, tests/unit/test_gap_coverage.py:8 |
| g2-coverage-audit.json | G2-ARCH-014 | P0 | done | 3. G2-P0 — Contract & Architecture Alignment | 2. Non-Negotiable Architectural Principles | EOIP-engg-doc-pkg/gaps2-requirements.md:112 | G2-ARCH-014 — Source permissions respected | packages/eoip/gaps/g2_architecture.py:3, packages/eoip/gaps/g2_architecture.py:84, packages/eoip/gaps/g2_readiness.py:8 | tests/unit/test_g2_readiness.py:5, tests/unit/test_gap_coverage.py:8 |
| g2-coverage-audit.json | G2-ARCH-015 | P0 | done | 3. G2-P0 — Contract & Architecture Alignment | 2. Non-Negotiable Architectural Principles | EOIP-engg-doc-pkg/gaps2-requirements.md:116 | G2-ARCH-015 — Progressive complexity | packages/eoip/gaps/g2_architecture.py:3, packages/eoip/gaps/g2_architecture.py:85, packages/eoip/gaps/g2_readiness.py:8 | tests/unit/test_g2_readiness.py:5, tests/unit/test_gap_coverage.py:8, tests/unit/test_gap_coverage.py:115 |
| g2-coverage-audit.json | G2-EKAF-003 | P2 | done | 3. G2-P0 — Contract & Architecture Alignment | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:187 | G2-EKAF-003 — SourceEvent envelope | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/contract/test_g2_contracts.py:45, tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EVENT-001 | P2 | done | 3. G2-P0 — Contract & Architecture Alignment | 8. Semantic Event Bus / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:832 | G2-EVENT-001 | packages/eoip/gaps/g2_readiness.py:13, packages/eoip/gaps/g2_readiness.py:124 | tests/unit/test_g2_readiness.py:10 |
| g2-coverage-audit.json | G2-EVOL-009 | P2 | done | 3. G2-P0 — Contract & Architecture Alignment | 6. Graph Evolution Engine | EOIP-engg-doc-pkg/gaps2-requirements.md:736 | G2-EVOL-009 | packages/eoip/contracts/revision.py:1, packages/eoip/gaps/g2_readiness.py:14, packages/eoip/gaps/g2_readiness.py:122 | tests/unit/test_g2_readiness.py:11 |
| gap-coverage-audit.json | GAP-AGOV-001 | P0 | done | 3. Phase 0 — Architecture Foundation | 24. Agent & MCP Governance / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:714 | GAP-AGOV-001: Tool registry with versioned schemas | packages/eoip/gaps/enterprise_completion.py:11 | tests/unit/test_enterprise_gap_completion.py:4 |
| gap-coverage-audit.json | GAP-AGOV-002 | P0 | done | 3. Phase 0 — Architecture Foundation | 24. Agent & MCP Governance / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:715 | GAP-AGOV-002: Read/write/destructive risk classification | packages/eoip/gaps/enterprise_completion.py:11 | tests/unit/test_enterprise_gap_completion.py:4 |
| gap-coverage-audit.json | GAP-AGOV-003 | P0 | done | 3. Phase 0 — Architecture Foundation | 24. Agent & MCP Governance / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:716 | GAP-AGOV-003: Capability tokens or equivalent scoped tool authorization in future enterprise phases | packages/eoip/gaps/enterprise_completion.py:11 | tests/unit/test_enterprise_gap_completion.py:4 |
| gap-coverage-audit.json | GAP-AGOV-004 | P0 | done | 3. Phase 0 — Architecture Foundation | 24. Agent & MCP Governance / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:717 | GAP-AGOV-004: Human approval policy by risk | packages/eoip/gaps/enterprise_completion.py:11 | tests/unit/test_enterprise_gap_completion.py:4 |
| gap-coverage-audit.json | GAP-CP-001 | P2 | done | 3. Phase 0 — Architecture Foundation | 7. Enterprise Semantic Control Plane / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:399 | GAP-CP-001: Ontology is the semantic control plane, not merely another graph | packages/eoip/gaps/enterprise_completion.py:22 | tests/unit/test_enterprise_gap_completion.py:15 |
| gap-coverage-audit.json | GAP-CP-002 | P2 | done | 3. Phase 0 — Architecture Foundation | 7. Enterprise Semantic Control Plane / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:400 | GAP-CP-002: Maintain a canonical entity registry | packages/eoip/gaps/enterprise_completion.py:22 | tests/unit/test_enterprise_gap_completion.py:15 |
| gap-coverage-audit.json | GAP-CP-003 | P2 | done | 3. Phase 0 — Architecture Foundation | 7. Enterprise Semantic Control Plane / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:401 | GAP-CP-003: Maintain canonical relationship registry | packages/eoip/gaps/enterprise_completion.py:22 | tests/unit/test_enterprise_gap_completion.py:15 |
| gap-coverage-audit.json | GAP-CP-004 | P2 | done | 3. Phase 0 — Architecture Foundation | 7. Enterprise Semantic Control Plane / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:402 | GAP-CP-004: Maintain policy, validation, provenance and mapping metadata | packages/eoip/gaps/enterprise_completion.py:22 | tests/unit/test_enterprise_gap_completion.py:15 |
| gap-coverage-audit.json | GAP-CP-005 | P2 | done | 3. Phase 0 — Architecture Foundation | 7. Enterprise Semantic Control Plane / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:403 | GAP-CP-005: Every connector maps into canonical contracts | packages/eoip/gaps/enterprise_completion.py:22 | tests/unit/test_enterprise_gap_completion.py:15 |
| gap-coverage-audit.json | GAP-CP-006 | P2 | done | 3. Phase 0 — Architecture Foundation | 7. Enterprise Semantic Control Plane / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:404 | GAP-CP-006: Source-specific fields remain accessible without polluting the canonical ontology | packages/eoip/gaps/enterprise_completion.py:22 | tests/unit/test_enterprise_gap_completion.py:15 |
| gap-coverage-audit.json | GAP-CP-007 | P2 | done | 3. Phase 0 — Architecture Foundation | 7. Enterprise Semantic Control Plane / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:405 | GAP-CP-007: Every schema/ontology change is versioned and diffable | packages/eoip/gaps/enterprise_completion.py:22 | tests/unit/test_enterprise_gap_completion.py:15 |
| gap-coverage-audit.json | GAP-CP-008 | P2 | done | 3. Phase 0 — Architecture Foundation | 7. Enterprise Semantic Control Plane / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:406 | GAP-CP-008: Breaking schema changes require migration plans | packages/eoip/gaps/enterprise_completion.py:22 | tests/unit/test_enterprise_gap_completion.py:15 |
| gap-coverage-audit.json | GAP-CP-009 | P2 | done | 3. Phase 0 — Architecture Foundation | 7. Enterprise Semantic Control Plane / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:407 | GAP-CP-009: Semantic contracts are machine-readable and testable | packages/eoip/gaps/coverage.py:8 | tests/unit/test_gap_coverage.py:4, tests/unit/test_gap_coverage.py:37, tests/unit/test_gap_coverage.py:54 |
| gap-coverage-audit.json | GAP-DBAGNOSTIC-001 | P2 | done | 3. Phase 0 — Architecture Foundation | 4. Competitive Study / 4.10 Oracle RDF Graph / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:338 | GAP-DBAGNOSTIC-001: Keep ontology/domain contracts independent of any single graph database implementation | packages/eoip/gaps/enterprise_completion.py:23 | tests/unit/test_enterprise_gap_completion.py:16 |
| gap-coverage-audit.json | GAP-HG-001 | P0 | done | 3. Phase 0 — Architecture Foundation | 44. HugeGraph-Specific Hardening / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:1074 | GAP-HG-001: Abstract HugeGraph client behind repository interface | packages/eoip/gaps/enterprise_completion.py:32 | tests/unit/test_enterprise_gap_completion.py:25 |
| gap-coverage-audit.json | GAP-OBS-001 | P1 | done | 3. Phase 0 — Architecture Foundation | 32. Graph Observability / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:855 | GAP-OBS-001: Trace a request from UI → API → planner → HugeGraph → retriever → model → response | packages/eoip/future_scope.py:70, packages/eoip/future_scope.py:792, packages/eoip/gaps/enterprise_completion.py:43 | tests/unit/test_enterprise_gap_completion.py:36 |
| gap-coverage-audit.json | GAP-OBS-002 | P1 | done | 3. Phase 0 — Architecture Foundation | 32. Graph Observability / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:856 | GAP-OBS-002: Trace ingestion from source record → entity → edge → index | packages/eoip/future_scope.py:71, packages/eoip/future_scope.py:792, packages/eoip/gaps/enterprise_completion.py:43 | tests/unit/test_enterprise_gap_completion.py:36 |
| gap-coverage-audit.json | GAP-OBS-003 | P1 | done | 3. Phase 0 — Architecture Foundation | 32. Graph Observability / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:857 | GAP-OBS-003: Metrics per connector/query/agent/retriever | packages/eoip/future_scope.py:792, packages/eoip/observability/metrics.py:1, packages/eoip/observability/metrics.py:185 | tests/unit/test_extended_api_routes_pass2.py:5, tests/unit/test_metrics.py:1, tests/unit/test_metrics.py:5 |
| gap-coverage-audit.json | GAP-OBS-004 | P1 | done | 3. Phase 0 — Architecture Foundation | 32. Graph Observability / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:858 | GAP-OBS-004: Correlate logs, metrics and traces | packages/eoip/future_scope.py:72, packages/eoip/future_scope.py:792, packages/eoip/gaps/enterprise_completion.py:43 | tests/unit/test_enterprise_gap_completion.py:36 |
| gap-coverage-audit.json | GAP-OBS-005 | P1 | done | 3. Phase 0 — Architecture Foundation | 32. Graph Observability / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:859 | GAP-OBS-005: Graph-specific metrics: | packages/eoip/future_scope.py:73, packages/eoip/future_scope.py:792, packages/eoip/gaps/enterprise_completion.py:43 | tests/unit/test_enterprise_gap_completion.py:36 |
| gap-coverage-audit.json | GAP-PORT-001 | P2 | done | 3. Phase 0 — Architecture Foundation | 4. Competitive Study / 4.9 Amazon Neptune / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:320 | GAP-PORT-001: Export/import through open formats to reduce lock-in | packages/eoip/gaps/enterprise_completion.py:44 | tests/unit/test_enterprise_gap_completion.py:37 |
| g2-coverage-audit.json | G2-EKAF-001 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:155 | G2-EKAF-001 — Source Registry | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_acquisition_fabric.py:275, tests/unit/test_g2_readiness.py:9, tests/unit/test_source_registry.py:52 |
| g2-coverage-audit.json | G2-EKAF-002 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:175 | G2-EKAF-002 — Connector SDK | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-004 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:204 | G2-EKAF-004 — Baseline crawl | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-005 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:207 | G2-EKAF-005 — Incremental sync | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-006 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:215 | G2-EKAF-006 — Webhook/event ingestion | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-007 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:218 | G2-EKAF-007 — Poll fallback | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-008 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:221 | G2-EKAF-008 — Reconciliation crawl | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-009 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:224 | G2-EKAF-009 — Idempotency | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-010 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:227 | G2-EKAF-010 — Ordering tolerance | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-011 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:230 | G2-EKAF-011 — Rate limiting | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-012 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:238 | G2-EKAF-012 — Checkpointing | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-013 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:241 | G2-EKAF-013 — Replay | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-014 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:250 | G2-EKAF-014 — Dead-letter handling | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-015 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:259 | G2-EKAF-015 — Dry run | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-016 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:262 | G2-EKAF-016 — Source deletion semantics | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-017 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:265 | G2-EKAF-017 — Schema drift | packages/eoip/connectors/drift.py:1, packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_ekaf_drift.py:13, tests/unit/test_ekaf_drift.py:29, tests/unit/test_ekaf_drift.py:42 |
| g2-coverage-audit.json | G2-EKAF-018 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:272 | G2-EKAF-018 — Mapping drift | packages/eoip/connectors/drift.py:1, packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_ekaf_drift.py:72, tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-019 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:275 | G2-EKAF-019 — Crawl boundaries | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_acquisition_fabric.py:200, tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-020 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:287 | G2-EKAF-020 — Authentication isolation | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-021 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:290 | G2-EKAF-021 — Connector health | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9, tests/unit/test_source_registry.py:52 |
| g2-coverage-audit.json | G2-EKAF-022 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:301 | G2-EKAF-022 — Source priority | packages/eoip/connectors/conflicts.py:1, packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_ekaf_conflicts.py:8, tests/unit/test_ekaf_conflicts.py:40, tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-023 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:304 | G2-EKAF-023 — Permission-aware metadata | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-024 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:307 | G2-EKAF-024 — Content fingerprinting | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-025 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:310 | G2-EKAF-025 — Attachment handling | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-026 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:319 | G2-EKAF-026 — Incremental graph enrichment | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-027 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:322 | G2-EKAF-027 — Source capability introspection | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-028 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:334 | G2-EKAF-028 — Connector compatibility matrix | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9, tests/unit/test_source_registry.py:52 |
| g2-coverage-audit.json | G2-EKAF-029 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:337 | G2-EKAF-029 — Offline source fixture mode | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-EKAF-030 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:340 | G2-EKAF-030 — Source onboarding wizard | packages/eoip/gaps/g2_readiness.py:12, packages/eoip/gaps/g2_readiness.py:120 | tests/unit/test_g2_readiness.py:9 |
| g2-coverage-audit.json | G2-OBS-001 | P1 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 30. Observability Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:1702 | G2-OBS-001 | packages/eoip/gaps/g2_observability.py:3, packages/eoip/gaps/g2_observability.py:29, packages/eoip/gaps/g2_observability.py:59 | tests/unit/test_g2_readiness.py:24, tests/unit/test_gap_coverage.py:9, tests/unit/test_gap_coverage.py:140 |
| g2-coverage-audit.json | G2-OBS-002 | P1 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 30. Observability Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:1705 | G2-OBS-002 | packages/eoip/gaps/g2_observability.py:3, packages/eoip/gaps/g2_observability.py:30, packages/eoip/gaps/g2_observability.py:31 | tests/unit/test_g2_readiness.py:24, tests/unit/test_gap_coverage.py:9, tests/unit/test_gap_coverage.py:168 |
| g2-coverage-audit.json | G2-SEC-CRAWL-001 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 29. Security Requirements for Acquisition/Crawling | EOIP-engg-doc-pkg/gaps2-requirements.md:1662 | G2-SEC-CRAWL-001 | packages/eoip/gaps/g2_readiness.py:33, packages/eoip/gaps/g2_readiness.py:125 | tests/unit/test_acquisition_fabric.py:156, tests/unit/test_g2_readiness.py:30 |
| g2-coverage-audit.json | G2-SEC-CRAWL-002 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 29. Security Requirements for Acquisition/Crawling | EOIP-engg-doc-pkg/gaps2-requirements.md:1665 | G2-SEC-CRAWL-002 | packages/eoip/gaps/g2_readiness.py:33, packages/eoip/gaps/g2_readiness.py:125 | tests/unit/test_acquisition_fabric.py:156, tests/unit/test_acquisition_fabric.py:172, tests/unit/test_g2_readiness.py:30 |
| g2-coverage-audit.json | G2-SEC-CRAWL-003 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 29. Security Requirements for Acquisition/Crawling | EOIP-engg-doc-pkg/gaps2-requirements.md:1668 | G2-SEC-CRAWL-003 | packages/eoip/gaps/g2_readiness.py:33, packages/eoip/gaps/g2_readiness.py:125 | tests/unit/test_g2_readiness.py:30 |
| g2-coverage-audit.json | G2-SEC-CRAWL-004 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 29. Security Requirements for Acquisition/Crawling | EOIP-engg-doc-pkg/gaps2-requirements.md:1671 | G2-SEC-CRAWL-004 | packages/eoip/gaps/g2_readiness.py:33, packages/eoip/gaps/g2_readiness.py:125 | tests/unit/test_g2_readiness.py:30 |
| g2-coverage-audit.json | G2-SEC-CRAWL-005 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 29. Security Requirements for Acquisition/Crawling | EOIP-engg-doc-pkg/gaps2-requirements.md:1674 | G2-SEC-CRAWL-005 | packages/eoip/gaps/g2_readiness.py:33, packages/eoip/gaps/g2_readiness.py:125 | tests/unit/test_g2_readiness.py:30 |
| g2-coverage-audit.json | G2-SEC-CRAWL-006 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 29. Security Requirements for Acquisition/Crawling | EOIP-engg-doc-pkg/gaps2-requirements.md:1677 | G2-SEC-CRAWL-006 | packages/eoip/gaps/g2_readiness.py:33, packages/eoip/gaps/g2_readiness.py:125 | tests/unit/test_g2_readiness.py:30 |
| g2-coverage-audit.json | G2-SEC-CRAWL-007 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 29. Security Requirements for Acquisition/Crawling | EOIP-engg-doc-pkg/gaps2-requirements.md:1680 | G2-SEC-CRAWL-007 | packages/eoip/gaps/g2_readiness.py:33, packages/eoip/gaps/g2_readiness.py:125 | tests/unit/test_g2_readiness.py:30 |
| g2-coverage-audit.json | G2-SEC-CRAWL-008 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 29. Security Requirements for Acquisition/Crawling | EOIP-engg-doc-pkg/gaps2-requirements.md:1683 | G2-SEC-CRAWL-008 | packages/eoip/gaps/g2_readiness.py:33, packages/eoip/gaps/g2_readiness.py:125 | tests/unit/test_g2_readiness.py:30 |
| g2-coverage-audit.json | G2-SEC-CRAWL-009 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 29. Security Requirements for Acquisition/Crawling | EOIP-engg-doc-pkg/gaps2-requirements.md:1686 | G2-SEC-CRAWL-009 | packages/eoip/gaps/g2_readiness.py:33, packages/eoip/gaps/g2_readiness.py:125 | tests/unit/test_g2_readiness.py:30 |
| g2-coverage-audit.json | G2-SEC-CRAWL-010 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 29. Security Requirements for Acquisition/Crawling | EOIP-engg-doc-pkg/gaps2-requirements.md:1689 | G2-SEC-CRAWL-010 | packages/eoip/gaps/g2_readiness.py:33, packages/eoip/gaps/g2_readiness.py:125 | tests/unit/test_g2_readiness.py:30 |
| g2-coverage-audit.json | G2-SEC-CRAWL-011 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 29. Security Requirements for Acquisition/Crawling | EOIP-engg-doc-pkg/gaps2-requirements.md:1692 | G2-SEC-CRAWL-011 | packages/eoip/gaps/g2_readiness.py:33, packages/eoip/gaps/g2_readiness.py:125 | tests/unit/test_g2_readiness.py:30 |
| g2-coverage-audit.json | G2-SEC-CRAWL-012 | P2 | done | 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 29. Security Requirements for Acquisition/Crawling | EOIP-engg-doc-pkg/gaps2-requirements.md:1695 | G2-SEC-CRAWL-012 | packages/eoip/gaps/g2_readiness.py:33, packages/eoip/gaps/g2_readiness.py:125 | tests/unit/test_g2_readiness.py:30 |
| gap-coverage-audit.json | GAP-HG-002 | P0 | done | 4. Phase 1 — Fully Functional Demonstrable MVP | 44. HugeGraph-Specific Hardening / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:1075 | GAP-HG-002: Automated schema migration | packages/eoip/gaps/enterprise_completion.py:32 | tests/unit/test_enterprise_gap_completion.py:25 |
| gap-coverage-audit.json | GAP-HG-003 | P0 | done | 4. Phase 1 — Fully Functional Demonstrable MVP | 44. HugeGraph-Specific Hardening / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:1076 | GAP-HG-003: Index advisor | packages/eoip/gaps/enterprise_completion.py:32 | tests/unit/test_enterprise_gap_completion.py:25 |
| gap-coverage-audit.json | GAP-HG-004 | P0 | done | 4. Phase 1 — Fully Functional Demonstrable MVP | 44. HugeGraph-Specific Hardening / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:1077 | GAP-HG-004: Bulk-loader path | packages/eoip/gaps/enterprise_completion.py:32 | tests/unit/test_bulk_load.py:1, tests/unit/test_bulk_load.py:44, tests/unit/test_bulk_load.py:95 |
| gap-coverage-audit.json | GAP-HG-005 | P0 | done | 4. Phase 1 — Fully Functional Demonstrable MVP | 44. HugeGraph-Specific Hardening / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:1078 | GAP-HG-005: Online ingestion path | packages/eoip/gaps/enterprise_completion.py:32 | tests/unit/test_enterprise_gap_completion.py:25 |
| gap-coverage-audit.json | GAP-KRAG-001 | P0 | done | 4. Phase 1 — Fully Functional Demonstrable MVP | 22. Knowledge-Aware GraphRAG / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:676 | GAP-KRAG-001: Retrieval must be ontology-aware | packages/eoip/gaps/enterprise_completion.py:36 | tests/unit/test_enterprise_gap_completion.py:29 |
| gap-coverage-audit.json | GAP-OFFLINE-001 | P0 | done | 4. Phase 1 — Fully Functional Demonstrable MVP | 4. Competitive Study / 4.9 Amazon Neptune / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:319 | GAP-OFFLINE-001: Zero mandatory Internet/cloud dependency | packages/eoip/gaps/enterprise_completion.py:44 | tests/unit/test_enterprise_gap_completion.py:37 |
| gap-coverage-audit.json | GAP-PROV-001 | P0 | done | 4. Phase 1 — Fully Functional Demonstrable MVP | 10. Provenance & Evidence Ledger / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:454 | GAP-PROV-001: Represent Entity, Activity and Agent provenance concepts | packages/eoip/provenance/evidence.py:7 | tests/unit/test_gap_governance_controls.py:20, tests/unit/test_gap_governance_controls.py:109 |
| gap-coverage-audit.json | GAP-PROV-002 | P0 | done | 4. Phase 1 — Fully Functional Demonstrable MVP | 10. Provenance & Evidence Ledger / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:455 | GAP-PROV-002: Every inferred edge must reference the evidence used | packages/eoip/provenance/evidence.py:8 | tests/unit/test_gap_governance_controls.py:21, tests/unit/test_gap_governance_controls.py:110 |
| gap-coverage-audit.json | GAP-PROV-003 | P0 | done | 4. Phase 1 — Fully Functional Demonstrable MVP | 10. Provenance & Evidence Ledger / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:456 | GAP-PROV-003: Preserve extraction algorithm/model/parser version | packages/eoip/provenance/evidence.py:9 | tests/unit/test_gap_governance_controls.py:22, tests/unit/test_gap_governance_controls.py:111 |
| gap-coverage-audit.json | GAP-PROV-004 | P0 | done | 4. Phase 1 — Fully Functional Demonstrable MVP | 10. Provenance & Evidence Ledger / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:457 | GAP-PROV-004: Preserve source checksum/version | packages/eoip/provenance/evidence.py:10 | tests/unit/test_gap_governance_controls.py:23, tests/unit/test_gap_governance_controls.py:112 |
| gap-coverage-audit.json | GAP-PROV-005 | P0 | done | 4. Phase 1 — Fully Functional Demonstrable MVP | 10. Provenance & Evidence Ledger / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:458 | GAP-PROV-005: Support graph-path evidence bundles | packages/eoip/gaps/enterprise_completion.py:45 | tests/unit/test_enterprise_gap_completion.py:38 |
| gap-coverage-audit.json | GAP-PROV-006 | P0 | done | 4. Phase 1 — Fully Functional Demonstrable MVP | 10. Provenance & Evidence Ledger / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:459 | GAP-PROV-006: Every AI answer returns an Evidence Manifest | packages/eoip/provenance/evidence.py:11 | tests/unit/test_gap_governance_controls.py:24, tests/unit/test_gap_governance_controls.py:113, tests/unit/test_gap_governance_controls.py:176 |
| gap-coverage-audit.json | GAP-QI-007 | P1 | done | 4. Phase 1 — Fully Functional Demonstrable MVP | 33. Query Intelligence / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:879 | GAP-QI-007: Saved parameterized query templates | packages/eoip/query/intelligence.py:9, packages/eoip/query/intelligence.py:381, packages/eoip/query/intelligence.py:433 | tests/unit/test_query_intelligence.py:1, tests/unit/test_query_intelligence.py:149 |
| gap-coverage-audit.json | GAP-SDT-001 | P0 | done | 4. Phase 1 — Fully Functional Demonstrable MVP | 6. Semantic Digital Thread / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:381 | GAP-SDT-001: Every requirement must be linkable to design, story, commit, code symbol, test, build, deployment, service and incident | packages/eoip/gaps/enterprise_completion.py:49 | tests/unit/test_enterprise_gap_completion.py:42, tests/unit/test_gap_coverage.py:43, tests/unit/test_gap_coverage.py:48 |
| gap-coverage-audit.json | GAP-SDT-002 | P0 | done | 4. Phase 1 — Fully Functional Demonstrable MVP | 6. Semantic Digital Thread / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:382 | GAP-SDT-002: Support forward and reverse navigation | packages/eoip/gaps/enterprise_completion.py:49 | tests/unit/test_enterprise_gap_completion.py:42 |
| gap-coverage-audit.json | GAP-SDT-003 | P0 | done | 4. Phase 1 — Fully Functional Demonstrable MVP | 6. Semantic Digital Thread / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:383 | GAP-SDT-003: Each link must have provenance, confidence and evidence | packages/eoip/gaps/enterprise_completion.py:49 | tests/unit/test_enterprise_gap_completion.py:42 |
| gap-coverage-audit.json | GAP-SDT-004 | P0 | done | 4. Phase 1 — Fully Functional Demonstrable MVP | 6. Semantic Digital Thread / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:384 | GAP-SDT-004: Provide missing-link detection | packages/eoip/gaps/enterprise_completion.py:49 | tests/unit/test_enterprise_gap_completion.py:42 |
| g2-coverage-audit.json | G2-EVENT-002 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 8. Semantic Event Bus / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:835 | G2-EVENT-002 | packages/eoip/gaps/g2_readiness.py:13, packages/eoip/gaps/g2_readiness.py:124 | tests/unit/test_g2_readiness.py:10 |
| g2-coverage-audit.json | G2-EVENT-003 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 8. Semantic Event Bus / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:838 | G2-EVENT-003 | packages/eoip/gaps/g2_readiness.py:13, packages/eoip/gaps/g2_readiness.py:124 | tests/unit/test_g2_readiness.py:10 |
| g2-coverage-audit.json | G2-EVENT-004 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 8. Semantic Event Bus / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:841 | G2-EVENT-004 | packages/eoip/gaps/g2_readiness.py:13, packages/eoip/gaps/g2_readiness.py:124 | tests/unit/test_g2_readiness.py:10 |
| g2-coverage-audit.json | G2-EVENT-005 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 8. Semantic Event Bus / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:844 | G2-EVENT-005 | packages/eoip/gaps/g2_readiness.py:13, packages/eoip/gaps/g2_readiness.py:124 | tests/unit/test_g2_readiness.py:10 |
| g2-coverage-audit.json | G2-EVENT-006 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 8. Semantic Event Bus / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:855 | G2-EVENT-006 | packages/eoip/gaps/g2_readiness.py:13, packages/eoip/gaps/g2_readiness.py:124 | tests/unit/test_g2_readiness.py:10 |
| g2-coverage-audit.json | G2-EVENT-007 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 8. Semantic Event Bus / Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:858 | G2-EVENT-007 | packages/eoip/gaps/g2_readiness.py:13, packages/eoip/gaps/g2_readiness.py:124 | tests/unit/test_g2_readiness.py:10 |
| g2-coverage-audit.json | G2-EVOL-001 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 6. Graph Evolution Engine | EOIP-engg-doc-pkg/gaps2-requirements.md:703 | G2-EVOL-001 | packages/eoip/gaps/g2_readiness.py:14, packages/eoip/gaps/g2_readiness.py:122 | tests/unit/test_g2_readiness.py:11 |
| g2-coverage-audit.json | G2-EVOL-002 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 6. Graph Evolution Engine | EOIP-engg-doc-pkg/gaps2-requirements.md:706 | G2-EVOL-002 | packages/eoip/gaps/g2_readiness.py:14, packages/eoip/gaps/g2_readiness.py:122 | tests/unit/test_g2_readiness.py:11 |
| g2-coverage-audit.json | G2-EVOL-003 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 6. Graph Evolution Engine | EOIP-engg-doc-pkg/gaps2-requirements.md:711 | G2-EVOL-003 | packages/eoip/gaps/g2_readiness.py:14, packages/eoip/gaps/g2_readiness.py:122 | tests/unit/test_g2_readiness.py:11 |
| g2-coverage-audit.json | G2-EVOL-004 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 6. Graph Evolution Engine | EOIP-engg-doc-pkg/gaps2-requirements.md:714 | G2-EVOL-004 | packages/eoip/gaps/g2_readiness.py:14, packages/eoip/gaps/g2_readiness.py:122 | tests/unit/test_g2_readiness.py:11 |
| g2-coverage-audit.json | G2-EVOL-005 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 6. Graph Evolution Engine | EOIP-engg-doc-pkg/gaps2-requirements.md:717 | G2-EVOL-005 | packages/eoip/gaps/g2_readiness.py:14, packages/eoip/gaps/g2_readiness.py:122 | tests/unit/test_g2_readiness.py:11 |
| g2-coverage-audit.json | G2-EVOL-006 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 6. Graph Evolution Engine | EOIP-engg-doc-pkg/gaps2-requirements.md:720 | G2-EVOL-006 | packages/eoip/gaps/g2_readiness.py:14, packages/eoip/gaps/g2_readiness.py:122 | tests/unit/test_g2_readiness.py:11 |
| g2-coverage-audit.json | G2-EVOL-007 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 6. Graph Evolution Engine | EOIP-engg-doc-pkg/gaps2-requirements.md:723 | G2-EVOL-007 | packages/eoip/gaps/g2_readiness.py:14, packages/eoip/gaps/g2_readiness.py:122 | tests/unit/test_g2_readiness.py:11 |
| g2-coverage-audit.json | G2-EVOL-008 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 6. Graph Evolution Engine | EOIP-engg-doc-pkg/gaps2-requirements.md:726 | G2-EVOL-008 | packages/eoip/gaps/g2_readiness.py:14, packages/eoip/gaps/g2_readiness.py:122 | tests/unit/test_g2_readiness.py:11 |
| g2-coverage-audit.json | G2-EVOL-010 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 6. Graph Evolution Engine | EOIP-engg-doc-pkg/gaps2-requirements.md:743 | G2-EVOL-010 | packages/eoip/gaps/g2_readiness.py:14, packages/eoip/gaps/g2_readiness.py:122 | tests/unit/test_bulk_load.py:1, tests/unit/test_bulk_load.py:44, tests/unit/test_bulk_load.py:95 |
| g2-coverage-audit.json | G2-EVOL-011 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 6. Graph Evolution Engine | EOIP-engg-doc-pkg/gaps2-requirements.md:746 | G2-EVOL-011 | packages/eoip/gaps/g2_readiness.py:14, packages/eoip/gaps/g2_readiness.py:122 | tests/unit/test_g2_readiness.py:11 |
| g2-coverage-audit.json | G2-EVOL-012 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 6. Graph Evolution Engine | EOIP-engg-doc-pkg/gaps2-requirements.md:749 | G2-EVOL-012 | packages/eoip/gaps/g2_readiness.py:14, packages/eoip/gaps/g2_readiness.py:122 | tests/unit/test_g2_readiness.py:11 |
| g2-coverage-audit.json | G2-EVOL-013 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 6. Graph Evolution Engine | EOIP-engg-doc-pkg/gaps2-requirements.md:752 | G2-EVOL-013 | packages/eoip/gaps/g2_readiness.py:14, packages/eoip/gaps/g2_readiness.py:122 | tests/unit/test_g2_readiness.py:11 |
| g2-coverage-audit.json | G2-EVOL-014 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 6. Graph Evolution Engine | EOIP-engg-doc-pkg/gaps2-requirements.md:755 | G2-EVOL-014 | packages/eoip/gaps/g2_readiness.py:14, packages/eoip/gaps/g2_readiness.py:122 | tests/unit/test_g2_readiness.py:11 |
| g2-coverage-audit.json | G2-EVOL-015 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 6. Graph Evolution Engine | EOIP-engg-doc-pkg/gaps2-requirements.md:758 | G2-EVOL-015 | packages/eoip/gaps/g2_readiness.py:14, packages/eoip/gaps/g2_readiness.py:122 | tests/unit/test_g2_readiness.py:11 |
| g2-coverage-audit.json | G2-EVOL-016 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 6. Graph Evolution Engine | EOIP-engg-doc-pkg/gaps2-requirements.md:761 | G2-EVOL-016 | packages/eoip/gaps/g2_readiness.py:14, packages/eoip/gaps/g2_readiness.py:122 | tests/unit/test_g2_readiness.py:11 |
| g2-coverage-audit.json | G2-JOURNAL-001 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 7. Semantic Change Journal | EOIP-engg-doc-pkg/gaps2-requirements.md:773 | G2-JOURNAL-001 | packages/eoip/gaps/g2_readiness.py:25, packages/eoip/gaps/g2_readiness.py:123 | tests/unit/test_g2_readiness.py:22 |
| g2-coverage-audit.json | G2-JOURNAL-002 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 7. Semantic Change Journal | EOIP-engg-doc-pkg/gaps2-requirements.md:776 | G2-JOURNAL-002 | packages/eoip/gaps/g2_readiness.py:25, packages/eoip/gaps/g2_readiness.py:123 | tests/unit/test_g2_readiness.py:22 |
| g2-coverage-audit.json | G2-JOURNAL-003 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 7. Semantic Change Journal | EOIP-engg-doc-pkg/gaps2-requirements.md:789 | G2-JOURNAL-003 | packages/eoip/gaps/g2_readiness.py:25, packages/eoip/gaps/g2_readiness.py:123 | tests/unit/test_g2_readiness.py:22 |
| g2-coverage-audit.json | G2-JOURNAL-004 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 7. Semantic Change Journal | EOIP-engg-doc-pkg/gaps2-requirements.md:797 | G2-JOURNAL-004 | packages/eoip/gaps/g2_readiness.py:25, packages/eoip/gaps/g2_readiness.py:123 | tests/unit/test_g2_readiness.py:22 |
| g2-coverage-audit.json | G2-JOURNAL-005 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 7. Semantic Change Journal | EOIP-engg-doc-pkg/gaps2-requirements.md:800 | G2-JOURNAL-005 | packages/eoip/gaps/g2_readiness.py:25, packages/eoip/gaps/g2_readiness.py:123 | tests/unit/test_g2_readiness.py:22 |
| g2-coverage-audit.json | G2-JOURNAL-006 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 7. Semantic Change Journal | EOIP-engg-doc-pkg/gaps2-requirements.md:803 | G2-JOURNAL-006 | packages/eoip/gaps/g2_readiness.py:25, packages/eoip/gaps/g2_readiness.py:123 | tests/unit/test_g2_readiness.py:22 |
| g2-coverage-audit.json | G2-REL-001 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 32. Reliability & Recovery | EOIP-engg-doc-pkg/gaps2-requirements.md:1763 | G2-REL-001 | packages/eoip/gaps/g2_readiness.py:32, packages/eoip/gaps/g2_readiness.py:262 | tests/unit/test_g2_readiness.py:29 |
| g2-coverage-audit.json | G2-REL-002 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 32. Reliability & Recovery | EOIP-engg-doc-pkg/gaps2-requirements.md:1766 | G2-REL-002 | packages/eoip/gaps/g2_readiness.py:32, packages/eoip/gaps/g2_readiness.py:262 | tests/unit/test_g2_readiness.py:29 |
| g2-coverage-audit.json | G2-REL-003 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 32. Reliability & Recovery | EOIP-engg-doc-pkg/gaps2-requirements.md:1769 | G2-REL-003 | packages/eoip/gaps/g2_readiness.py:32, packages/eoip/gaps/g2_readiness.py:262 | tests/unit/test_g2_readiness.py:29 |
| g2-coverage-audit.json | G2-REL-004 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 32. Reliability & Recovery | EOIP-engg-doc-pkg/gaps2-requirements.md:1772 | G2-REL-004 | packages/eoip/gaps/g2_readiness.py:32, packages/eoip/gaps/g2_readiness.py:262 | tests/unit/test_g2_readiness.py:29 |
| g2-coverage-audit.json | G2-REL-005 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 32. Reliability & Recovery | EOIP-engg-doc-pkg/gaps2-requirements.md:1775 | G2-REL-005 | packages/eoip/gaps/g2_readiness.py:32, packages/eoip/gaps/g2_readiness.py:262 | tests/unit/test_g2_readiness.py:29, tests/unit/test_graph_evolution.py:232 |
| g2-coverage-audit.json | G2-REL-006 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 32. Reliability & Recovery | EOIP-engg-doc-pkg/gaps2-requirements.md:1778 | G2-REL-006 | packages/eoip/gaps/g2_readiness.py:32, packages/eoip/gaps/g2_readiness.py:262 | tests/unit/test_g2_readiness.py:29 |
| g2-coverage-audit.json | G2-REL-007 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 32. Reliability & Recovery | EOIP-engg-doc-pkg/gaps2-requirements.md:1781 | G2-REL-007 | packages/eoip/gaps/g2_readiness.py:32, packages/eoip/gaps/g2_readiness.py:262 | tests/unit/test_g2_readiness.py:29, tests/unit/test_operational_recovery.py:36, tests/unit/test_recovery_bundle.py:48 |
| g2-coverage-audit.json | G2-REL-008 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 32. Reliability & Recovery | EOIP-engg-doc-pkg/gaps2-requirements.md:1784 | G2-REL-008 | packages/eoip/gaps/g2_readiness.py:32, packages/eoip/gaps/g2_readiness.py:262 | tests/unit/test_g2_readiness.py:29 |
| g2-coverage-audit.json | G2-SYNC-001 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 5. Baseline, Incremental Synchronization & Reconciliation | EOIP-engg-doc-pkg/gaps2-requirements.md:642 | G2-SYNC-001 — Baseline state | packages/eoip/gaps/g2_readiness.py:52, packages/eoip/gaps/g2_readiness.py:121 | tests/unit/test_g2_readiness.py:49 |
| g2-coverage-audit.json | G2-SYNC-002 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 5. Baseline, Incremental Synchronization & Reconciliation | EOIP-engg-doc-pkg/gaps2-requirements.md:645 | G2-SYNC-002 — Baseline snapshot | packages/eoip/gaps/g2_readiness.py:52, packages/eoip/gaps/g2_readiness.py:121 | tests/unit/test_g2_readiness.py:49 |
| g2-coverage-audit.json | G2-SYNC-003 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 5. Baseline, Incremental Synchronization & Reconciliation | EOIP-engg-doc-pkg/gaps2-requirements.md:655 | G2-SYNC-003 — Delta processing | packages/eoip/gaps/g2_readiness.py:52, packages/eoip/gaps/g2_readiness.py:121 | tests/unit/test_g2_readiness.py:49 |
| g2-coverage-audit.json | G2-SYNC-004 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 5. Baseline, Incremental Synchronization & Reconciliation | EOIP-engg-doc-pkg/gaps2-requirements.md:658 | G2-SYNC-004 — Delete/retire | packages/eoip/gaps/g2_readiness.py:52, packages/eoip/gaps/g2_readiness.py:121 | tests/unit/test_g2_readiness.py:49 |
| g2-coverage-audit.json | G2-SYNC-005 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 5. Baseline, Incremental Synchronization & Reconciliation | EOIP-engg-doc-pkg/gaps2-requirements.md:661 | G2-SYNC-005 — Missed-event recovery | packages/eoip/gaps/g2_readiness.py:52, packages/eoip/gaps/g2_readiness.py:121 | tests/unit/test_g2_readiness.py:49 |
| g2-coverage-audit.json | G2-SYNC-006 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 5. Baseline, Incremental Synchronization & Reconciliation | EOIP-engg-doc-pkg/gaps2-requirements.md:664 | G2-SYNC-006 — Duplicate-event handling | packages/eoip/gaps/g2_readiness.py:52, packages/eoip/gaps/g2_readiness.py:121 | tests/unit/test_g2_readiness.py:49 |
| g2-coverage-audit.json | G2-SYNC-007 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 5. Baseline, Incremental Synchronization & Reconciliation | EOIP-engg-doc-pkg/gaps2-requirements.md:667 | G2-SYNC-007 — Late event handling | packages/eoip/gaps/g2_readiness.py:52, packages/eoip/gaps/g2_readiness.py:121 | tests/unit/test_g2_readiness.py:49 |
| g2-coverage-audit.json | G2-SYNC-008 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 5. Baseline, Incremental Synchronization & Reconciliation | EOIP-engg-doc-pkg/gaps2-requirements.md:670 | G2-SYNC-008 — Dependency-aware update | packages/eoip/gaps/g2_readiness.py:52, packages/eoip/gaps/g2_readiness.py:121 | tests/unit/test_g2_readiness.py:49 |
| g2-coverage-audit.json | G2-SYNC-009 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 5. Baseline, Incremental Synchronization & Reconciliation | EOIP-engg-doc-pkg/gaps2-requirements.md:673 | G2-SYNC-009 — Consistency watermark | packages/eoip/gaps/g2_readiness.py:52, packages/eoip/gaps/g2_readiness.py:121 | tests/unit/test_g2_readiness.py:49 |
| g2-coverage-audit.json | G2-SYNC-010 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 5. Baseline, Incremental Synchronization & Reconciliation | EOIP-engg-doc-pkg/gaps2-requirements.md:676 | G2-SYNC-010 — Full rebuild is exceptional | packages/eoip/gaps/g2_readiness.py:52, packages/eoip/gaps/g2_readiness.py:121 | tests/unit/test_g2_readiness.py:49 |
| g2-coverage-audit.json | G2-SYNC-011 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 5. Baseline, Incremental Synchronization & Reconciliation | EOIP-engg-doc-pkg/gaps2-requirements.md:679 | G2-SYNC-011 — Rebuild equivalence test | packages/eoip/gaps/g2_readiness.py:52, packages/eoip/gaps/g2_readiness.py:121 | tests/unit/test_g2_readiness.py:49 |
| g2-coverage-audit.json | G2-SYNC-012 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 5. Baseline, Incremental Synchronization & Reconciliation | EOIP-engg-doc-pkg/gaps2-requirements.md:682 | G2-SYNC-012 — Connector pause/resume | packages/eoip/gaps/g2_readiness.py:52, packages/eoip/gaps/g2_readiness.py:121 | tests/unit/test_g2_readiness.py:49 |
| g2-coverage-audit.json | G2-SYNC-013 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 5. Baseline, Incremental Synchronization & Reconciliation | EOIP-engg-doc-pkg/gaps2-requirements.md:685 | G2-SYNC-013 — Backfill | packages/eoip/gaps/g2_readiness.py:52, packages/eoip/gaps/g2_readiness.py:121 | tests/unit/test_g2_readiness.py:49 |
| g2-coverage-audit.json | G2-SYNC-014 | P2 | done | 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 5. Baseline, Incremental Synchronization & Reconciliation | EOIP-engg-doc-pkg/gaps2-requirements.md:688 | G2-SYNC-014 — Selective rescan | packages/eoip/gaps/g2_readiness.py:52, packages/eoip/gaps/g2_readiness.py:121 | tests/unit/test_g2_readiness.py:49 |
| gap-coverage-audit.json | GAP-CONTRACT-001 | P2 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 9. Semantic Contract Testing / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:439 | GAP-CONTRACT-001: Define contracts between source systems and ontology mappings | packages/eoip/gaps/enterprise_completion.py:20 | tests/unit/test_enterprise_gap_completion.py:13 |
| gap-coverage-audit.json | GAP-CONTRACT-002 | P2 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 9. Semantic Contract Testing / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:440 | GAP-CONTRACT-002: Detect connector schema drift | packages/eoip/gaps/enterprise_completion.py:20 | tests/unit/test_enterprise_gap_completion.py:13 |
| gap-coverage-audit.json | GAP-CONTRACT-003 | P2 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 9. Semantic Contract Testing / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:441 | GAP-CONTRACT-003: Fail or quarantine ingestion when required semantic invariants are violated | packages/eoip/gaps/enterprise_completion.py:20 | tests/unit/test_enterprise_gap_completion.py:13 |
| gap-coverage-audit.json | GAP-CONTRACT-004 | P2 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 9. Semantic Contract Testing / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:442 | GAP-CONTRACT-004: Generate compatibility reports before deploying ontology changes | packages/eoip/gaps/enterprise_completion.py:20 | tests/unit/test_enterprise_gap_completion.py:13 |
| gap-coverage-audit.json | GAP-CONTRACT-005 | P2 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 9. Semantic Contract Testing / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:443 | GAP-CONTRACT-005: Maintain producer/consumer mapping contracts | packages/eoip/gaps/enterprise_completion.py:20 | tests/unit/test_enterprise_gap_completion.py:13 |
| gap-coverage-audit.json | GAP-CONTRACT-006 | P2 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 9. Semantic Contract Testing / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:444 | GAP-CONTRACT-006: Expose contract tests to CI/CD | packages/eoip/gaps/enterprise_completion.py:21 | tests/unit/test_enterprise_gap_completion.py:14 |
| gap-coverage-audit.json | GAP-GITOPS-001 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 8. Ontology GitOps / Semantic DevOps / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:417 | GAP-GITOPS-001: Store ontology/schema source definitions in Git-compatible text formats | packages/eoip/ontology/gitops.py:1 | tests/unit/test_ontology_gitops.py:1 |
| gap-coverage-audit.json | GAP-GITOPS-002 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 8. Ontology GitOps / Semantic DevOps / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:418 | GAP-GITOPS-002: Provide ontology branch, pull-request/review and merge workflows | packages/eoip/ontology/gitops.py:1 | tests/unit/test_ontology_gitops.py:1 |
| gap-coverage-audit.json | GAP-GITOPS-003 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 8. Ontology GitOps / Semantic DevOps / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:419 | GAP-GITOPS-003: Generate semantic diffs: | packages/eoip/ontology/gitops.py:1, apps/api/main.py:1209 | tests/unit/test_ontology_gitops.py:1 |
| gap-coverage-audit.json | GAP-GITOPS-004 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 8. Ontology GitOps / Semantic DevOps / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:427 | GAP-GITOPS-004: CI validates ontology before publishing | packages/eoip/ontology/gitops.py:1, packages/eoip/ontology/gitops.py:169 | tests/unit/test_ontology_gitops.py:1 |
| gap-coverage-audit.json | GAP-GITOPS-005 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 8. Ontology GitOps / Semantic DevOps / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:428 | GAP-GITOPS-005: Run impact analysis for ontology changes | packages/eoip/ontology/gitops.py:1 | tests/unit/test_ontology_gitops.py:1 |
| gap-coverage-audit.json | GAP-GITOPS-006 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 8. Ontology GitOps / Semantic DevOps / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:429 | GAP-GITOPS-006: Generate migration scripts | packages/eoip/ontology/gitops.py:1 | tests/unit/test_ontology_gitops.py:1 |
| gap-coverage-audit.json | GAP-GITOPS-007 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 8. Ontology GitOps / Semantic DevOps / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:430 | GAP-GITOPS-007: Allow rollback to previous semantic version | packages/eoip/ontology/gitops.py:1 | tests/unit/test_ontology_gitops.py:1 |
| gap-coverage-audit.json | GAP-GITOPS-008 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 8. Ontology GitOps / Semantic DevOps / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:431 | GAP-GITOPS-008: Package ontology releases using SemVer-like policy | packages/eoip/ontology/gitops.py:1 | tests/unit/test_ontology_gitops.py:1 |
| gap-coverage-audit.json | GAP-GOV-001 | P2 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 4. Competitive Study / 4.4 TopBraid EDG / TQ Data Foundation / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:197 | GAP-GOV-001: Add semantic stewardship workflow: draft → review → approve → publish → deprecate | packages/eoip/future_scope.py:14, packages/eoip/future_scope.py:44, packages/eoip/future_scope.py:296 | tests/unit/test_enterprise_gap_completion.py:23 |
| gap-coverage-audit.json | GAP-GOV-002 | P2 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 4. Competitive Study / 4.4 TopBraid EDG / TQ Data Foundation / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:198 | GAP-GOV-002: Support ontology branches, diffs, merge conflict detection and semantic merge | packages/eoip/future_scope.py:14, packages/eoip/future_scope.py:45, packages/eoip/future_scope.py:318 | tests/unit/test_enterprise_gap_completion.py:23 |
| gap-coverage-audit.json | GAP-GOV-003 | P2 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 4. Competitive Study / 4.4 TopBraid EDG / TQ Data Foundation / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:199 | GAP-GOV-003: Add business glossary, taxonomy, reference-data and ontology crosswalks | packages/eoip/gaps/enterprise_completion.py:30, packages/eoip/ontology/skos.py:4, packages/eoip/ontology/skos.py:94 | tests/unit/test_enterprise_gap_completion.py:23 |
| gap-coverage-audit.json | GAP-KQ-001 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 12. Knowledge Quality SLOs / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:489 | GAP-KQ-001: Define per-domain quality SLOs | packages/eoip/gaps/enterprise_completion.py:35 | tests/unit/test_enterprise_gap_completion.py:28 |
| gap-coverage-audit.json | GAP-KQ-002 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 12. Knowledge Quality SLOs / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:490 | GAP-KQ-002: Compute: | packages/eoip/gaps/enterprise_completion.py:35 | tests/unit/test_enterprise_gap_completion.py:28 |
| gap-coverage-audit.json | GAP-KQ-003 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 12. Knowledge Quality SLOs / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:502 | GAP-KQ-003: Quality SLO violations generate actionable findings | packages/eoip/gaps/enterprise_completion.py:35 | tests/unit/test_enterprise_gap_completion.py:28 |
| gap-coverage-audit.json | GAP-KQ-004 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 12. Knowledge Quality SLOs / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:503 | GAP-KQ-004: Quality score is not one opaque number; show component dimensions | packages/eoip/gaps/enterprise_completion.py:35 | tests/unit/test_enterprise_gap_completion.py:28 |
| gap-coverage-audit.json | GAP-KQ-005 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 12. Knowledge Quality SLOs / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:504 | GAP-KQ-005: Quality must be measurable by source, project, graph, domain and release | packages/eoip/gaps/enterprise_completion.py:35 | tests/unit/test_enterprise_gap_completion.py:28 |
| gap-coverage-audit.json | GAP-KQ-006 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 12. Knowledge Quality SLOs / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:505 | GAP-KQ-006: Support trend charts and regression gates | packages/eoip/gaps/enterprise_completion.py:35 | tests/unit/test_enterprise_gap_completion.py:28 |
| gap-coverage-audit.json | GAP-STUDIO-001 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 18. Ontology Studio & Collaborative Knowledge Engineering / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:603 | GAP-STUDIO-001: Visual class/property/relationship editor | packages/eoip/gaps/enterprise_completion.py:52 | tests/unit/test_enterprise_gap_completion.py:45 |
| gap-coverage-audit.json | GAP-STUDIO-002 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 18. Ontology Studio & Collaborative Knowledge Engineering / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:604 | GAP-STUDIO-002: Text source view for experts | packages/eoip/gaps/enterprise_completion.py:52, apps/web/src/studio/Studio.jsx:11 | tests/unit/test_enterprise_gap_completion.py:45 |
| gap-coverage-audit.json | GAP-STUDIO-003 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 18. Ontology Studio & Collaborative Knowledge Engineering / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:605 | GAP-STUDIO-003: SHACL-style validation rules | packages/eoip/gaps/enterprise_completion.py:52, apps/web/src/studio/Studio.jsx:12 | tests/unit/test_enterprise_gap_completion.py:45 |
| gap-coverage-audit.json | GAP-STUDIO-004 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 18. Ontology Studio & Collaborative Knowledge Engineering / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:606 | GAP-STUDIO-004: RDFS/OWL export | packages/eoip/gaps/enterprise_completion.py:52 | tests/unit/test_enterprise_gap_completion.py:45 |
| gap-coverage-audit.json | GAP-STUDIO-005 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 18. Ontology Studio & Collaborative Knowledge Engineering / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:607 | GAP-STUDIO-005: SKOS taxonomy support | packages/eoip/ontology/skos.py:3 | tests/unit/test_skos_taxonomy.py:1 |
| gap-coverage-audit.json | GAP-STUDIO-006 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 18. Ontology Studio & Collaborative Knowledge Engineering / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:608 | GAP-STUDIO-006: Diff/merge | packages/eoip/gaps/enterprise_completion.py:52 | tests/unit/test_enterprise_gap_completion.py:45 |
| gap-coverage-audit.json | GAP-STUDIO-007 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 18. Ontology Studio & Collaborative Knowledge Engineering / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:609 | GAP-STUDIO-007: Comments and review workflow | packages/eoip/gaps/enterprise_completion.py:53 | tests/unit/test_enterprise_gap_completion.py:46 |
| gap-coverage-audit.json | GAP-STUDIO-008 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 18. Ontology Studio & Collaborative Knowledge Engineering / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:610 | GAP-STUDIO-008: Reusable ontology modules | packages/eoip/gaps/enterprise_completion.py:53 | tests/unit/test_enterprise_gap_completion.py:46 |
| gap-coverage-audit.json | GAP-STUDIO-009 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 18. Ontology Studio & Collaborative Knowledge Engineering / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:611 | GAP-STUDIO-009: Crosswalk/mapping designer | packages/eoip/gaps/enterprise_completion.py:53 | tests/unit/test_enterprise_gap_completion.py:46 |
| gap-coverage-audit.json | GAP-STUDIO-010 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 18. Ontology Studio & Collaborative Knowledge Engineering / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:612 | GAP-STUDIO-010: Impact preview before publish | packages/eoip/gaps/enterprise_completion.py:53 | tests/unit/test_enterprise_gap_completion.py:46 |
| gap-coverage-audit.json | GAP-STUDIO-011 | P0 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 18. Ontology Studio & Collaborative Knowledge Engineering / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:613 | GAP-STUDIO-011: Generate forms and API schemas from ontology where practical | packages/eoip/gaps/enterprise_completion.py:53, packages/eoip/ontology/schema_gen.py:1 | tests/unit/test_enterprise_gap_completion.py:46 |
| gap-coverage-audit.json | GAP-TAX-001 | P1 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 4. Competitive Study / 4.5 PoolParty Semantic Suite / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:221 | GAP-TAX-001: Add enterprise taxonomy/thesaurus management using SKOS-compatible concepts | packages/eoip/ontology/skos.py:3, packages/eoip/ontology/skos.py:33, packages/eoip/ontology/skos.py:49 | tests/unit/test_skos_taxonomy.py:1 |
| gap-coverage-audit.json | GAP-TRUST-001 | P1 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 26. Knowledge Quarantine & Trust Zones / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:750 | GAP-TRUST-001: New/inferred/untrusted knowledge enters a quarantine zone | packages/eoip/provenance/trust.py:4 | tests/unit/test_gap_governance_controls.py:14, tests/unit/test_gap_governance_controls.py:77 |
| gap-coverage-audit.json | GAP-TRUST-002 | P1 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 26. Knowledge Quarantine & Trust Zones / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:751 | GAP-TRUST-002: Promotion requires rules, confidence or approval | packages/eoip/provenance/trust.py:5 | tests/unit/test_gap_governance_controls.py:15, tests/unit/test_gap_governance_controls.py:78 |
| gap-coverage-audit.json | GAP-TRUST-003 | P1 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 26. Knowledge Quarantine & Trust Zones / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:752 | GAP-TRUST-003: Trust states: | packages/eoip/provenance/trust.py:6 | tests/unit/test_gap_governance_controls.py:16, tests/unit/test_gap_governance_controls.py:79, tests/unit/test_gap_governance_controls.py:175 |
| gap-coverage-audit.json | GAP-TRUST-004 | P1 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 26. Knowledge Quarantine & Trust Zones / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:760 | GAP-TRUST-004: Queries may specify minimum trust level | packages/eoip/provenance/trust.py:7 | tests/unit/test_gap_governance_controls.py:17, tests/unit/test_gap_governance_controls.py:80 |
| gap-coverage-audit.json | GAP-TRUST-005 | P1 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 26. Knowledge Quarantine & Trust Zones / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:761 | GAP-TRUST-005: AI answers must disclose use of non-certified knowledge | packages/eoip/provenance/trust.py:8 | tests/unit/test_gap_governance_controls.py:18, tests/unit/test_gap_governance_controls.py:81, tests/unit/test_gap_governance_controls.py:117 |
| gap-coverage-audit.json | GAP-TRUTH-001 | P1 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 11. Confidence, Contradiction & Truth Management / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:470 | GAP-TRUTH-001: Do not overwrite conflicting claims | packages/eoip/truth/engine.py:2, packages/eoip/truth/engine.py:29, packages/eoip/truth/models.py:3 | tests/unit/test_truth_claims.py:1 |
| gap-coverage-audit.json | GAP-TRUTH-002 | P1 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 11. Confidence, Contradiction & Truth Management / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:471 | GAP-TRUTH-002: Represent claims separately from resolved canonical facts | packages/eoip/truth/engine.py:2, packages/eoip/truth/models.py:3, packages/eoip/truth/__init__.py:1 | tests/unit/test_truth_claims.py:1 |
| gap-coverage-audit.json | GAP-TRUTH-003 | P1 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 11. Confidence, Contradiction & Truth Management / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:472 | GAP-TRUTH-003: Store source authority score | packages/eoip/truth/engine.py:2, packages/eoip/truth/models.py:3, packages/eoip/truth/__init__.py:1 | tests/unit/test_truth_claims.py:1 |
| gap-coverage-audit.json | GAP-TRUTH-004 | P1 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 11. Confidence, Contradiction & Truth Management / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:473 | GAP-TRUTH-004: Store extraction confidence | packages/eoip/truth/engine.py:2, packages/eoip/truth/models.py:3, packages/eoip/truth/__init__.py:1 | tests/unit/test_truth_claims.py:1 |
| gap-coverage-audit.json | GAP-TRUTH-005 | P1 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 11. Confidence, Contradiction & Truth Management / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:474 | GAP-TRUTH-005: Store validation confidence | packages/eoip/truth/engine.py:2, packages/eoip/truth/models.py:3, packages/eoip/truth/__init__.py:1 | tests/unit/test_truth_claims.py:1 |
| gap-coverage-audit.json | GAP-TRUTH-006 | P1 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 11. Confidence, Contradiction & Truth Management / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:475 | GAP-TRUTH-006: Detect contradictory claims | packages/eoip/truth/engine.py:2, packages/eoip/truth/models.py:3, packages/eoip/truth/__init__.py:1 | tests/unit/test_truth_claims.py:1 |
| gap-coverage-audit.json | GAP-TRUTH-007 | P1 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 11. Confidence, Contradiction & Truth Management / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:476 | GAP-TRUTH-007: Support configurable truth-resolution policy | packages/eoip/truth/engine.py:2, packages/eoip/truth/models.py:3, packages/eoip/truth/__init__.py:1 | tests/unit/test_truth_claims.py:1 |
| gap-coverage-audit.json | GAP-TRUTH-008 | P1 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 11. Confidence, Contradiction & Truth Management / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:477 | GAP-TRUTH-008: Permit human adjudication | packages/eoip/truth/engine.py:2, packages/eoip/truth/models.py:3, packages/eoip/truth/__init__.py:1 | tests/unit/test_truth_claims.py:1 |
| gap-coverage-audit.json | GAP-TRUTH-009 | P1 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 11. Confidence, Contradiction & Truth Management / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:478 | GAP-TRUTH-009: Retain rejected/obsolete claims for history | packages/eoip/truth/engine.py:2, packages/eoip/truth/models.py:3, packages/eoip/truth/__init__.py:1 | tests/unit/test_truth_claims.py:1 |
| gap-coverage-audit.json | GAP-TRUTH-010 | P1 | done | 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 11. Confidence, Contradiction & Truth Management / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:479 | GAP-TRUTH-010: Explain why a canonical fact was selected | packages/eoip/truth/engine.py:2, packages/eoip/truth/models.py:3, packages/eoip/truth/__init__.py:1 | tests/unit/test_truth_claims.py:1 |
| g2-coverage-audit.json | G2-SRC-CODE-001 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.7 Local Git / Source Code | EOIP-engg-doc-pkg/gaps2-requirements.md:458 | G2-SRC-CODE-001 | packages/eoip/gaps/g2_readiness.py:38, packages/eoip/gaps/g2_readiness.py:151 | tests/unit/test_g2_readiness.py:35 |
| g2-coverage-audit.json | G2-SRC-CODE-002 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.7 Local Git / Source Code | EOIP-engg-doc-pkg/gaps2-requirements.md:461 | G2-SRC-CODE-002 | packages/eoip/gaps/g2_readiness.py:38, packages/eoip/gaps/g2_readiness.py:151 | tests/unit/test_g2_readiness.py:35 |
| g2-coverage-audit.json | G2-SRC-CODE-003 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.7 Local Git / Source Code | EOIP-engg-doc-pkg/gaps2-requirements.md:464 | G2-SRC-CODE-003 | packages/eoip/gaps/g2_readiness.py:38, packages/eoip/gaps/g2_readiness.py:151 | tests/unit/test_g2_readiness.py:35 |
| g2-coverage-audit.json | G2-SRC-CODE-004 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.7 Local Git / Source Code | EOIP-engg-doc-pkg/gaps2-requirements.md:467 | G2-SRC-CODE-004 | packages/eoip/gaps/g2_readiness.py:38, packages/eoip/gaps/g2_readiness.py:151 | tests/unit/test_g2_readiness.py:35 |
| g2-coverage-audit.json | G2-SRC-CODE-005 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.7 Local Git / Source Code | EOIP-engg-doc-pkg/gaps2-requirements.md:470 | G2-SRC-CODE-005 | packages/eoip/gaps/g2_readiness.py:38, packages/eoip/gaps/g2_readiness.py:151 | tests/unit/test_g2_readiness.py:35 |
| g2-coverage-audit.json | G2-SRC-GH-001 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.5 GitHub | EOIP-engg-doc-pkg/gaps2-requirements.md:426 | G2-SRC-GH-001 | packages/eoip/gaps/g2_readiness.py:41, packages/eoip/gaps/g2_readiness.py:149, packages/eoip/ingestion/github.py:1 | tests/unit/test_g2_readiness.py:38 |
| g2-coverage-audit.json | G2-SRC-GH-002 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.5 GitHub | EOIP-engg-doc-pkg/gaps2-requirements.md:429 | G2-SRC-GH-002 | packages/eoip/gaps/g2_readiness.py:41, packages/eoip/gaps/g2_readiness.py:149, packages/eoip/ingestion/github.py:1 | tests/unit/test_acquisition_fabric.py:411, tests/unit/test_g2_readiness.py:38 |
| g2-coverage-audit.json | G2-SRC-GH-003 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.5 GitHub | EOIP-engg-doc-pkg/gaps2-requirements.md:432 | G2-SRC-GH-003 | packages/eoip/gaps/g2_readiness.py:41, packages/eoip/gaps/g2_readiness.py:149, packages/eoip/ingestion/github.py:1 | tests/unit/test_g2_readiness.py:38 |
| g2-coverage-audit.json | G2-SRC-GH-004 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.5 GitHub | EOIP-engg-doc-pkg/gaps2-requirements.md:435 | G2-SRC-GH-004 | packages/eoip/gaps/g2_readiness.py:41, packages/eoip/gaps/g2_readiness.py:149, packages/eoip/ingestion/github.py:1 | tests/unit/test_g2_readiness.py:38 |
| g2-coverage-audit.json | G2-SRC-GL-001 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.6 GitLab | EOIP-engg-doc-pkg/gaps2-requirements.md:442 | G2-SRC-GL-001 | packages/eoip/gaps/g2_readiness.py:42, packages/eoip/gaps/g2_readiness.py:150, packages/eoip/ingestion/gitlab_rest.py:1 | tests/unit/test_g2_readiness.py:39 |
| g2-coverage-audit.json | G2-SRC-GL-002 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.6 GitLab | EOIP-engg-doc-pkg/gaps2-requirements.md:445 | G2-SRC-GL-002 | packages/eoip/gaps/g2_readiness.py:42, packages/eoip/gaps/g2_readiness.py:150, packages/eoip/ingestion/gitlab_rest.py:1 | tests/unit/test_acquisition_fabric.py:463, tests/unit/test_g2_readiness.py:39 |
| g2-coverage-audit.json | G2-SRC-GL-003 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.6 GitLab | EOIP-engg-doc-pkg/gaps2-requirements.md:448 | G2-SRC-GL-003 | packages/eoip/gaps/g2_readiness.py:42, packages/eoip/gaps/g2_readiness.py:150, packages/eoip/ingestion/gitlab_rest.py:1 | tests/unit/test_g2_readiness.py:39 |
| g2-coverage-audit.json | G2-SRC-GL-004 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.6 GitLab | EOIP-engg-doc-pkg/gaps2-requirements.md:451 | G2-SRC-GL-004 | packages/eoip/gaps/g2_readiness.py:42, packages/eoip/gaps/g2_readiness.py:150, packages/eoip/ingestion/gitlab_rest.py:1 | tests/unit/test_g2_readiness.py:39 |
| g2-coverage-audit.json | G2-SRC-JIRA-001 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.1 Jira | EOIP-engg-doc-pkg/gaps2-requirements.md:350 | G2-SRC-JIRA-001 | packages/eoip/gaps/g2_readiness.py:44, packages/eoip/gaps/g2_readiness.py:145, packages/eoip/ingestion/jira_rest.py:1 | tests/unit/test_g2_readiness.py:41 |
| g2-coverage-audit.json | G2-SRC-JIRA-002 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.1 Jira | EOIP-engg-doc-pkg/gaps2-requirements.md:353 | G2-SRC-JIRA-002 | packages/eoip/gaps/g2_readiness.py:44, packages/eoip/gaps/g2_readiness.py:145, packages/eoip/ingestion/jira_rest.py:1 | tests/unit/test_g2_readiness.py:41 |
| g2-coverage-audit.json | G2-SRC-JIRA-003 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.1 Jira | EOIP-engg-doc-pkg/gaps2-requirements.md:356 | G2-SRC-JIRA-003 | packages/eoip/gaps/g2_readiness.py:44, packages/eoip/gaps/g2_readiness.py:145, packages/eoip/ingestion/jira_rest.py:1 | tests/unit/test_g2_readiness.py:41 |
| g2-coverage-audit.json | G2-SRC-JIRA-004 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.1 Jira | EOIP-engg-doc-pkg/gaps2-requirements.md:359 | G2-SRC-JIRA-004 | packages/eoip/gaps/g2_readiness.py:44, packages/eoip/gaps/g2_readiness.py:145, packages/eoip/ingestion/jira_rest.py:1 | tests/unit/test_g2_readiness.py:41 |
| g2-coverage-audit.json | G2-SRC-JIRA-005 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.1 Jira | EOIP-engg-doc-pkg/gaps2-requirements.md:362 | G2-SRC-JIRA-005 | packages/eoip/gaps/g2_readiness.py:44, packages/eoip/gaps/g2_readiness.py:145, packages/eoip/ingestion/jira_rest.py:1 | tests/unit/test_g2_readiness.py:41 |
| g2-coverage-audit.json | G2-SRC-JIRA-006 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.1 Jira | EOIP-engg-doc-pkg/gaps2-requirements.md:365 | G2-SRC-JIRA-006 | packages/eoip/gaps/g2_readiness.py:44, packages/eoip/gaps/g2_readiness.py:145, packages/eoip/ingestion/jira_rest.py:1 | tests/unit/test_g2_readiness.py:41, tests/unit/test_gap_coverage.py:65 |
| g2-coverage-audit.json | G2-SRC-WEB-001 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.16 Generic Files / Intranet / Web | EOIP-engg-doc-pkg/gaps2-requirements.md:623 | G2-SRC-WEB-001 | packages/eoip/gaps/g2_readiness.py:51, packages/eoip/gaps/g2_readiness.py:160 | tests/unit/test_g2_readiness.py:48 |
| g2-coverage-audit.json | G2-SRC-WEB-002 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.16 Generic Files / Intranet / Web | EOIP-engg-doc-pkg/gaps2-requirements.md:626 | G2-SRC-WEB-002 | packages/eoip/gaps/g2_readiness.py:51, packages/eoip/gaps/g2_readiness.py:160 | tests/unit/test_acquisition_fabric.py:172, tests/unit/test_g2_readiness.py:48 |
| g2-coverage-audit.json | G2-SRC-WEB-003 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.16 Generic Files / Intranet / Web | EOIP-engg-doc-pkg/gaps2-requirements.md:629 | G2-SRC-WEB-003 | packages/eoip/gaps/g2_readiness.py:51, packages/eoip/gaps/g2_readiness.py:160 | tests/unit/test_g2_readiness.py:48 |
| g2-coverage-audit.json | G2-SRC-WEB-004 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.16 Generic Files / Intranet / Web | EOIP-engg-doc-pkg/gaps2-requirements.md:632 | G2-SRC-WEB-004 | packages/eoip/gaps/g2_readiness.py:51, packages/eoip/gaps/g2_readiness.py:160 | tests/unit/test_g2_readiness.py:48 |
| g2-coverage-audit.json | G2-SRC-WEB-005 | P2 | done | 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 4.16 Generic Files / Intranet / Web | EOIP-engg-doc-pkg/gaps2-requirements.md:635 | G2-SRC-WEB-005 | packages/eoip/gaps/g2_readiness.py:51, packages/eoip/gaps/g2_readiness.py:160 | tests/unit/test_g2_readiness.py:48 |
| gap-coverage-audit.json | GAP-ARCH-001 | P0 | done | 6. Phase 3 — Enterprise Engineering Intelligence | 14. Architecture Conformance Engine / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:529 | GAP-ARCH-001: Allow architecture rules such as: | packages/eoip/gaps/enterprise_completion.py:16 | tests/unit/test_enterprise_gap_completion.py:9 |
| gap-coverage-audit.json | GAP-ARCH-002 | P0 | done | 6. Phase 3 — Enterprise Engineering Intelligence | 14. Architecture Conformance Engine / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:535 | GAP-ARCH-002: Evaluate actual code/deployment graph against intended architecture | packages/eoip/gaps/enterprise_completion.py:16 | tests/unit/test_enterprise_gap_completion.py:9 |
| gap-coverage-audit.json | GAP-ARCH-003 | P0 | done | 6. Phase 3 — Enterprise Engineering Intelligence | 14. Architecture Conformance Engine / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:536 | GAP-ARCH-003: Show violations in Web UI and VS Code | packages/eoip/gaps/enterprise_completion.py:16 | tests/unit/test_enterprise_gap_completion.py:9 |
| gap-coverage-audit.json | GAP-ARCH-004 | P0 | done | 6. Phase 3 — Enterprise Engineering Intelligence | 14. Architecture Conformance Engine / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:537 | GAP-ARCH-004: Support CI gate mode | packages/eoip/gaps/enterprise_completion.py:16 | tests/unit/test_enterprise_gap_completion.py:9 |
| gap-coverage-audit.json | GAP-ARCH-005 | P0 | done | 6. Phase 3 — Enterprise Engineering Intelligence | 14. Architecture Conformance Engine / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:538 | GAP-ARCH-005: Link violation to exact code symbols/commits | packages/eoip/gaps/enterprise_completion.py:16 | tests/unit/test_enterprise_gap_completion.py:9 |
| gap-coverage-audit.json | GAP-ARCH-006 | P0 | done | 6. Phase 3 — Enterprise Engineering Intelligence | 14. Architecture Conformance Engine / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:539 | GAP-ARCH-006: Provide trend and technical-debt history | packages/eoip/gaps/enterprise_completion.py:16 | tests/unit/test_enterprise_gap_completion.py:9 |
| gap-coverage-audit.json | GAP-CHANGE-001 | P0 | done | 6. Phase 3 — Enterprise Engineering Intelligence | 15. Change Intelligence & Semantic Blast Radius / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:547 | GAP-CHANGE-001: Analyze a proposed code change before merge | packages/eoip/gaps/enterprise_completion.py:19 | tests/unit/test_enterprise_gap_completion.py:12 |
| gap-coverage-audit.json | GAP-CHANGE-002 | P0 | done | 6. Phase 3 — Enterprise Engineering Intelligence | 15. Change Intelligence & Semantic Blast Radius / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:548 | GAP-CHANGE-002: Analyze a Jira/change request before implementation | packages/eoip/gaps/enterprise_completion.py:19 | tests/unit/test_enterprise_gap_completion.py:12 |
| gap-coverage-audit.json | GAP-CHANGE-003 | P0 | done | 6. Phase 3 — Enterprise Engineering Intelligence | 15. Change Intelligence & Semantic Blast Radius / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:549 | GAP-CHANGE-003: Traverse code, service, test, deployment, ownership and incident relationships | packages/eoip/gaps/enterprise_completion.py:19 | tests/unit/test_enterprise_gap_completion.py:12 |
| gap-coverage-audit.json | GAP-CHANGE-004 | P0 | done | 6. Phase 3 — Enterprise Engineering Intelligence | 15. Change Intelligence & Semantic Blast Radius / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:550 | GAP-CHANGE-004: Categorize impact: | packages/eoip/gaps/enterprise_completion.py:19 | tests/unit/test_enterprise_gap_completion.py:12 |
| gap-coverage-audit.json | GAP-CHANGE-005 | P0 | done | 6. Phase 3 — Enterprise Engineering Intelligence | 15. Change Intelligence & Semantic Blast Radius / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:559 | GAP-CHANGE-005: Provide confidence and supporting paths | packages/eoip/gaps/enterprise_completion.py:19 | tests/unit/test_enterprise_gap_completion.py:12 |
| gap-coverage-audit.json | GAP-CHANGE-006 | P0 | done | 6. Phase 3 — Enterprise Engineering Intelligence | 15. Change Intelligence & Semantic Blast Radius / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:560 | GAP-CHANGE-006: Compare predicted impact with actual post-deployment incidents to calibrate the model | packages/eoip/gaps/enterprise_completion.py:19 | tests/unit/test_enterprise_gap_completion.py:12 |
| gap-coverage-audit.json | GAP-FRESH-001 | P2 | done | 6. Phase 3 — Enterprise Engineering Intelligence | 40. Knowledge Freshness Engine / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:1001 | GAP-FRESH-001: Detect stale documents | packages/eoip/graph/expertise.py:1, apps/api/app.py:934 | tests/unit/test_expertise_freshness.py:1 |
| gap-coverage-audit.json | GAP-FRESH-002 | P2 | done | 6. Phase 3 — Enterprise Engineering Intelligence | 40. Knowledge Freshness Engine / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:1002 | GAP-FRESH-002: Detect docs contradicted by code/config/runtime | packages/eoip/graph/expertise.py:1, apps/api/app.py:934 | tests/unit/test_expertise_freshness.py:1 |
| gap-coverage-audit.json | GAP-FRESH-003 | P2 | done | 6. Phase 3 — Enterprise Engineering Intelligence | 40. Knowledge Freshness Engine / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:1003 | GAP-FRESH-003: Detect ownership changes | packages/eoip/graph/expertise.py:1, apps/api/app.py:934 | tests/unit/test_expertise_freshness.py:1 |
| gap-coverage-audit.json | GAP-FRESH-004 | P2 | done | 6. Phase 3 — Enterprise Engineering Intelligence | 40. Knowledge Freshness Engine / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:1004 | GAP-FRESH-004: Detect deprecated APIs still referenced in docs | packages/eoip/graph/expertise.py:1, apps/api/app.py:934 | tests/unit/test_expertise_freshness.py:1 |
| gap-coverage-audit.json | GAP-FRESH-005 | P2 | done | 6. Phase 3 — Enterprise Engineering Intelligence | 40. Knowledge Freshness Engine / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:1005 | GAP-FRESH-005: Recommend review—not silently rewrite authoritative docs | packages/eoip/graph/expertise.py:1, apps/api/app.py:934 | tests/unit/test_expertise_freshness.py:1 |
| gap-coverage-audit.json | GAP-SDT-005 | P0 | done | 6. Phase 3 — Enterprise Engineering Intelligence | 6. Semantic Digital Thread / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:385 | GAP-SDT-005: Generate traceability coverage percentage per project/release | packages/eoip/gaps/enterprise_completion.py:49 | tests/unit/test_enterprise_gap_completion.py:42 |
| gap-coverage-audit.json | GAP-SDT-006 | P0 | done | 6. Phase 3 — Enterprise Engineering Intelligence | 6. Semantic Digital Thread / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:386 | GAP-SDT-006: Provide release-level “traceability completeness” gates | packages/eoip/gaps/enterprise_completion.py:49 | tests/unit/test_enterprise_gap_completion.py:42 |
| gap-coverage-audit.json | GAP-SDT-007 | P0 | done | 6. Phase 3 — Enterprise Engineering Intelligence | 6. Semantic Digital Thread / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:387 | GAP-SDT-007: Maintain temporal state so historical releases can be reconstructed | packages/eoip/gaps/enterprise_completion.py:49 | tests/unit/test_enterprise_gap_completion.py:42 |
| gap-coverage-audit.json | GAP-SDT-008 | P0 | done | 6. Phase 3 — Enterprise Engineering Intelligence | 6. Semantic Digital Thread / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:388 | GAP-SDT-008: Support semantic digital-thread comparison between releases | packages/eoip/gaps/enterprise_completion.py:50 | tests/unit/test_enterprise_gap_completion.py:43 |
| g2-coverage-audit.json | G2-GRAPH-API-001 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 9.1 API & Contract Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:867 | G2-GRAPH-API-001 | packages/eoip/gaps/g2_readiness.py:15, packages/eoip/gaps/g2_readiness.py:182 | tests/unit/test_g2_readiness.py:12 |
| g2-coverage-audit.json | G2-GRAPH-API-002 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 9.1 API & Contract Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:870 | G2-GRAPH-API-002 | packages/eoip/gaps/g2_readiness.py:15, packages/eoip/gaps/g2_readiness.py:182 | tests/unit/test_g2_readiness.py:12 |
| g2-coverage-audit.json | G2-GRAPH-API-003 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 9.1 API & Contract Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:879 | G2-GRAPH-API-003 | packages/eoip/gaps/g2_readiness.py:15, packages/eoip/gaps/g2_readiness.py:182 | tests/unit/test_g2_readiness.py:12 |
| g2-coverage-audit.json | G2-SRC-API-001 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 4.8 API Portals / Contracts | EOIP-engg-doc-pkg/gaps2-requirements.md:477 | G2-SRC-API-001 | packages/eoip/gaps/g2_readiness.py:36, packages/eoip/gaps/g2_readiness.py:152 | tests/unit/test_g2_readiness.py:33 |
| g2-coverage-audit.json | G2-SRC-API-002 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 4.8 API Portals / Contracts | EOIP-engg-doc-pkg/gaps2-requirements.md:480 | G2-SRC-API-002 | packages/eoip/gaps/g2_readiness.py:36, packages/eoip/gaps/g2_readiness.py:152 | tests/unit/test_g2_readiness.py:33 |
| g2-coverage-audit.json | G2-SRC-API-003 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 4.8 API Portals / Contracts | EOIP-engg-doc-pkg/gaps2-requirements.md:483 | G2-SRC-API-003 | packages/eoip/gaps/g2_readiness.py:36, packages/eoip/gaps/g2_readiness.py:152 | tests/unit/test_g2_readiness.py:33 |
| g2-coverage-audit.json | G2-SRC-API-004 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 4.8 API Portals / Contracts | EOIP-engg-doc-pkg/gaps2-requirements.md:487 | G2-SRC-API-004 | packages/eoip/gaps/g2_readiness.py:36, packages/eoip/gaps/g2_readiness.py:152 | tests/unit/test_g2_readiness.py:33 |
| g2-coverage-audit.json | G2-SRC-API-005 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 4.8 API Portals / Contracts | EOIP-engg-doc-pkg/gaps2-requirements.md:490 | G2-SRC-API-005 | packages/eoip/gaps/g2_readiness.py:36, packages/eoip/gaps/g2_readiness.py:152 | tests/unit/test_g2_readiness.py:33 |
| g2-coverage-audit.json | G2-SRC-API-006 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 4.8 API Portals / Contracts | EOIP-engg-doc-pkg/gaps2-requirements.md:493 | G2-SRC-API-006 | packages/eoip/gaps/g2_readiness.py:36, packages/eoip/gaps/g2_readiness.py:152 | tests/unit/test_g2_readiness.py:33 |
| g2-coverage-audit.json | G2-SRC-CONF-001 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 4.2 Confluence / Enterprise Wiki | EOIP-engg-doc-pkg/gaps2-requirements.md:372 | G2-SRC-CONF-001 | packages/eoip/gaps/g2_readiness.py:39, packages/eoip/gaps/g2_readiness.py:146 | tests/runtime_dlq/test_confluence_acquisition.py:8, tests/unit/test_confluence_metadata.py:45, tests/unit/test_confluence_metadata.py:63 |
| g2-coverage-audit.json | G2-SRC-CONF-002 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 4.2 Confluence / Enterprise Wiki | EOIP-engg-doc-pkg/gaps2-requirements.md:375 | G2-SRC-CONF-002 | packages/eoip/gaps/g2_readiness.py:39, packages/eoip/gaps/g2_readiness.py:146 | tests/runtime_dlq/test_confluence_acquisition.py:8, tests/unit/test_confluence_history.py:45, tests/unit/test_confluence_history.py:87 |
| g2-coverage-audit.json | G2-SRC-CONF-003 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 4.2 Confluence / Enterprise Wiki | EOIP-engg-doc-pkg/gaps2-requirements.md:378 | G2-SRC-CONF-003 | packages/eoip/gaps/g2_readiness.py:39, packages/eoip/gaps/g2_readiness.py:146 | tests/runtime_dlq/test_confluence_acquisition.py:8, tests/unit/test_confluence_body.py:26, tests/unit/test_confluence_body.py:52 |
| g2-coverage-audit.json | G2-SRC-CONF-004 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 4.2 Confluence / Enterprise Wiki | EOIP-engg-doc-pkg/gaps2-requirements.md:381 | G2-SRC-CONF-004 | packages/eoip/gaps/g2_readiness.py:39, packages/eoip/gaps/g2_readiness.py:146 | tests/runtime_dlq/test_confluence_acquisition.py:8, tests/unit/test_document_references.py:47, tests/unit/test_document_references.py:79 |
| g2-coverage-audit.json | G2-SRC-CONF-005 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 4.2 Confluence / Enterprise Wiki | EOIP-engg-doc-pkg/gaps2-requirements.md:384 | G2-SRC-CONF-005 | packages/eoip/gaps/g2_readiness.py:39, packages/eoip/gaps/g2_readiness.py:146 | tests/runtime_dlq/test_confluence_acquisition.py:8, tests/unit/test_document_references.py:101, tests/unit/test_document_references.py:138 |
| g2-coverage-audit.json | G2-SRC-SNKB-001 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 4.3 ServiceNow Knowledge Base | EOIP-engg-doc-pkg/gaps2-requirements.md:391 | G2-SRC-SNKB-001 | packages/eoip/gaps/g2_readiness.py:49, packages/eoip/gaps/g2_readiness.py:147 | tests/unit/test_g2_readiness.py:46 |
| g2-coverage-audit.json | G2-SRC-SNKB-002 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 4.3 ServiceNow Knowledge Base | EOIP-engg-doc-pkg/gaps2-requirements.md:394 | G2-SRC-SNKB-002 | packages/eoip/gaps/g2_readiness.py:49, packages/eoip/gaps/g2_readiness.py:147 | tests/unit/test_g2_readiness.py:46 |
| g2-coverage-audit.json | G2-SRC-SNKB-003 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 4.3 ServiceNow Knowledge Base | EOIP-engg-doc-pkg/gaps2-requirements.md:397 | G2-SRC-SNKB-003 | packages/eoip/gaps/g2_readiness.py:49, packages/eoip/gaps/g2_readiness.py:147 | tests/unit/test_g2_readiness.py:46 |
| g2-coverage-audit.json | G2-SRC-SNOW-001 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 4.4 ServiceNow Incidents / Problems / Changes / CMDB | EOIP-engg-doc-pkg/gaps2-requirements.md:404 | G2-SRC-SNOW-001 | packages/eoip/gaps/g2_readiness.py:50, packages/eoip/gaps/g2_readiness.py:148 | tests/unit/test_g2_readiness.py:47 |
| g2-coverage-audit.json | G2-SRC-SNOW-002 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 4.4 ServiceNow Incidents / Problems / Changes / CMDB | EOIP-engg-doc-pkg/gaps2-requirements.md:407 | G2-SRC-SNOW-002 | packages/eoip/gaps/g2_readiness.py:50, packages/eoip/gaps/g2_readiness.py:148 | tests/unit/test_g2_readiness.py:47 |
| g2-coverage-audit.json | G2-SRC-SNOW-003 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 4.4 ServiceNow Incidents / Problems / Changes / CMDB | EOIP-engg-doc-pkg/gaps2-requirements.md:410 | G2-SRC-SNOW-003 | packages/eoip/gaps/g2_readiness.py:50, packages/eoip/gaps/g2_readiness.py:148 | tests/unit/test_g2_readiness.py:47 |
| g2-coverage-audit.json | G2-SRC-SNOW-004 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 4.4 ServiceNow Incidents / Problems / Changes / CMDB | EOIP-engg-doc-pkg/gaps2-requirements.md:413 | G2-SRC-SNOW-004 | packages/eoip/gaps/g2_readiness.py:50, packages/eoip/gaps/g2_readiness.py:148 | tests/unit/test_g2_readiness.py:47 |
| g2-coverage-audit.json | G2-SRC-SNOW-005 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 4.4 ServiceNow Incidents / Problems / Changes / CMDB | EOIP-engg-doc-pkg/gaps2-requirements.md:416 | G2-SRC-SNOW-005 | packages/eoip/gaps/g2_readiness.py:50, packages/eoip/gaps/g2_readiness.py:148 | tests/unit/test_g2_readiness.py:47 |
| g2-coverage-audit.json | G2-SRC-SNOW-006 | P2 | done | 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 4.4 ServiceNow Incidents / Problems / Changes / CMDB | EOIP-engg-doc-pkg/gaps2-requirements.md:419 | G2-SRC-SNOW-006 | packages/eoip/gaps/g2_readiness.py:50, packages/eoip/gaps/g2_readiness.py:148 | tests/unit/test_g2_readiness.py:47 |
| gap-coverage-audit.json | GAP-CACHE-001 | P2 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 34. Semantic Cache / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:888 | GAP-CACHE-001: Cache by normalized semantic intent/query plan rather than raw prompt only | packages/eoip/query/cache.py:1 | tests/unit/test_query_cache.py:1 |
| gap-coverage-audit.json | GAP-CACHE-002 | P2 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 34. Semantic Cache / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:889 | GAP-CACHE-002: Cache dependencies reference graph versions/source freshness | packages/eoip/future_scope.py:74, packages/eoip/future_scope.py:712, packages/eoip/query/cache.py:1 | tests/unit/test_query_cache.py:1 |
| gap-coverage-audit.json | GAP-CACHE-003 | P2 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 34. Semantic Cache / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:890 | GAP-CACHE-003: Invalidate using graph CDC | packages/eoip/future_scope.py:75, packages/eoip/future_scope.py:712, packages/eoip/query/cache.py:1 | tests/unit/test_query_cache.py:1 |
| gap-coverage-audit.json | GAP-CACHE-004 | P2 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 34. Semantic Cache / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:891 | GAP-CACHE-004: Separate deterministic query cache from AI response cache | packages/eoip/query/cache.py:1, packages/eoip/query/cache.py:8 | tests/unit/test_query_cache.py:1 |
| gap-coverage-audit.json | GAP-CACHE-005 | P2 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 34. Semantic Cache / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:892 | GAP-CACHE-005: Do not serve stale results beyond policy | packages/eoip/future_scope.py:76, packages/eoip/future_scope.py:712, packages/eoip/query/cache.py:1 | tests/unit/test_query_cache.py:1 |
| gap-coverage-audit.json | GAP-GRAG-001 | P2 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 4. Competitive Study / 4.11 Microsoft GraphRAG / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:358 | GAP-GRAG-001: Do not make LLM extraction the only path to graph construction | packages/eoip/gaps/enterprise_completion.py:31 | tests/unit/test_enterprise_gap_completion.py:24 |
| gap-coverage-audit.json | GAP-GRAG-002 | P2 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 4. Competitive Study / 4.11 Microsoft GraphRAG / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:359 | GAP-GRAG-002: Use deterministic source-system relations first; model-generated relations second | packages/eoip/gaps/enterprise_completion.py:31 | tests/unit/test_enterprise_gap_completion.py:24 |
| gap-coverage-audit.json | GAP-GRAG-003 | P2 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 4. Competitive Study / 4.11 Microsoft GraphRAG / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:360 | GAP-GRAG-003: Add community detection and hierarchical semantic summaries, but regenerate summaries incrementally rather than rebuilding the whole corpus | packages/eoip/gaps/enterprise_completion.py:31 | tests/unit/test_enterprise_gap_completion.py:24 |
| gap-coverage-audit.json | GAP-GRAG-004 | P2 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 4. Competitive Study / 4.11 Microsoft GraphRAG / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:361 | GAP-GRAG-004: Maintain cost/compute budgets even for local models | packages/eoip/gaps/enterprise_completion.py:31 | tests/unit/test_enterprise_gap_completion.py:24 |
| gap-coverage-audit.json | GAP-GRAG-005 | P2 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 4. Competitive Study / 4.11 Microsoft GraphRAG / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:362 | GAP-GRAG-005: Benchmark GraphRAG against direct graph query, vector RAG, hybrid RAG and no-RAG baselines | packages/eoip/gaps/enterprise_completion.py:31 | tests/unit/test_enterprise_gap_completion.py:24 |
| gap-coverage-audit.json | GAP-GRAG-006 | P2 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 4. Competitive Study / 4.11 Microsoft GraphRAG / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:363 | GAP-GRAG-006: Persist evidence chains for every answer | packages/eoip/provenance/evidence.py:14 | tests/unit/test_gap_governance_controls.py:27, tests/unit/test_gap_governance_controls.py:116 |
| gap-coverage-audit.json | GAP-KRAG-002 | P0 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 22. Knowledge-Aware GraphRAG / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:677 | GAP-KRAG-002: Favor authoritative graph facts over generated summaries | packages/eoip/gaps/enterprise_completion.py:36 | tests/unit/test_enterprise_gap_completion.py:29 |
| gap-coverage-audit.json | GAP-KRAG-003 | P0 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 22. Knowledge-Aware GraphRAG / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:678 | GAP-KRAG-003: Community summaries must link to underlying nodes/edges | packages/eoip/gaps/enterprise_completion.py:36 | tests/unit/test_enterprise_gap_completion.py:29 |
| gap-coverage-audit.json | GAP-KRAG-004 | P0 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 22. Knowledge-Aware GraphRAG / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:679 | GAP-KRAG-004: Incremental community update | packages/eoip/gaps/enterprise_completion.py:36 | tests/unit/test_enterprise_gap_completion.py:29 |
| gap-coverage-audit.json | GAP-KRAG-005 | P0 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 22. Knowledge-Aware GraphRAG / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:680 | GAP-KRAG-005: Temporal filtering | packages/eoip/gaps/enterprise_completion.py:36 | tests/unit/test_enterprise_gap_completion.py:29 |
| gap-coverage-audit.json | GAP-KRAG-006 | P0 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 22. Knowledge-Aware GraphRAG / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:681 | GAP-KRAG-006: Contradiction-aware context assembly | packages/eoip/gaps/enterprise_completion.py:36 | tests/unit/test_enterprise_gap_completion.py:29 |
| gap-coverage-audit.json | GAP-KRAG-007 | P0 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 22. Knowledge-Aware GraphRAG / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:682 | GAP-KRAG-007: Answer abstention when evidence is insufficient | packages/eoip/graph/rag_router.py:51, packages/eoip/graph/rag_router.py:60, packages/eoip/graph/rag_router.py:79 | tests/unit/test_gap_governance_controls.py:26, tests/unit/test_gap_governance_controls.py:115, tests/unit/test_gap_governance_controls.py:177 |
| gap-coverage-audit.json | GAP-KRAG-008 | P0 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 22. Knowledge-Aware GraphRAG / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:683 | GAP-KRAG-008: Confidence calibrated from evidence—not model self-confidence | packages/eoip/gaps/enterprise_completion.py:37, packages/eoip/graph/rag_router.py:176 | tests/unit/test_enterprise_gap_completion.py:30 |
| gap-coverage-audit.json | GAP-KRAG-009 | P0 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 22. Knowledge-Aware GraphRAG / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:684 | GAP-KRAG-009: Every response includes evidence manifest | packages/eoip/gaps/enterprise_completion.py:37, packages/eoip/graph/rag_router.py:19, packages/eoip/graph/rag_router.py:35 | tests/unit/test_enterprise_gap_completion.py:30 |
| gap-coverage-audit.json | GAP-KRAG-010 | P0 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 22. Knowledge-Aware GraphRAG / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:685 | GAP-KRAG-010: Local model routing by task complexity | packages/eoip/gaps/enterprise_completion.py:37 | tests/unit/test_enterprise_gap_completion.py:30 |
| gap-coverage-audit.json | GAP-QI-001 | P1 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 33. Query Intelligence / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:873 | GAP-QI-001: Query plan explain | packages/eoip/query/intelligence.py:4, packages/eoip/query/intelligence.py:132, apps/api/extended.py:9 | tests/unit/test_query_intelligence.py:1, tests/unit/test_query_intelligence.py:39 |
| gap-coverage-audit.json | GAP-QI-002 | P1 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 33. Query Intelligence / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:874 | GAP-QI-002: Cost estimation | packages/eoip/query/intelligence.py:5, packages/eoip/query/intelligence.py:243, apps/api/extended.py:9 | tests/unit/test_query_intelligence.py:1, tests/unit/test_query_intelligence.py:71 |
| gap-coverage-audit.json | GAP-QI-003 | P1 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 33. Query Intelligence / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:875 | GAP-QI-003: Query history | packages/eoip/query/intelligence.py:6, packages/eoip/query/intelligence.py:297, apps/api/extended.py:9 | tests/unit/test_query_intelligence.py:1, tests/unit/test_query_intelligence.py:83 |
| gap-coverage-audit.json | GAP-QI-004 | P1 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 33. Query Intelligence / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:876 | GAP-QI-004: Slow-query analyzer | packages/eoip/query/intelligence.py:7, packages/eoip/query/intelligence.py:352, apps/api/extended.py:9 | tests/unit/test_query_intelligence.py:1, tests/unit/test_query_intelligence.py:114 |
| gap-coverage-audit.json | GAP-QI-005 | P1 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 33. Query Intelligence / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:877 | GAP-QI-005: Suggested indexes | packages/eoip/query/intelligence.py:7, apps/api/extended.py:9, apps/api/extended.py:594 | tests/unit/test_query_intelligence.py:1 |
| gap-coverage-audit.json | GAP-QI-006 | P1 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 33. Query Intelligence / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:878 | GAP-QI-006: Traversal-risk detector | packages/eoip/query/intelligence.py:8, packages/eoip/query/intelligence.py:278, apps/api/extended.py:9 | tests/unit/test_query_intelligence.py:1 |
| gap-coverage-audit.json | GAP-QI-008 | P1 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 33. Query Intelligence / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:880 | GAP-QI-008: Natural-language query produces editable structured plan before execution when risk is high | packages/eoip/query/intelligence.py:10, apps/api/extended.py:9, apps/api/extended.py:594 | tests/unit/test_query_intelligence.py:1 |
| gap-coverage-audit.json | GAP-RET-001 | P0 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 21. Unified Retrieval Fabric / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:655 | GAP-RET-001: Implement retrieval router | packages/eoip/gaps/enterprise_completion.py:47 | tests/unit/test_enterprise_gap_completion.py:40 |
| gap-coverage-audit.json | GAP-RET-002 | P0 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 21. Unified Retrieval Fabric / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:656 | GAP-RET-002: Candidate retrievers: | packages/eoip/gaps/enterprise_completion.py:47, packages/eoip/retrieval/service.py:283, packages/eoip/retrieval/service.py:300 | tests/unit/test_enterprise_gap_completion.py:40 |
| gap-coverage-audit.json | GAP-RET-003 | P0 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 21. Unified Retrieval Fabric / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:665 | GAP-RET-003: Rank using evidence quality, recency, authority and relevance | packages/eoip/gaps/enterprise_completion.py:47, packages/eoip/retrieval/service.py:160, packages/eoip/retrieval/service.py:323 | tests/unit/test_enterprise_gap_completion.py:40 |
| gap-coverage-audit.json | GAP-RET-004 | P0 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 21. Unified Retrieval Fabric / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:666 | GAP-RET-004: Query planner chooses minimal sufficient retrieval path | packages/eoip/gaps/enterprise_completion.py:47 | tests/unit/test_enterprise_gap_completion.py:40 |
| gap-coverage-audit.json | GAP-RET-005 | P0 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 21. Unified Retrieval Fabric / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:667 | GAP-RET-005: Evaluate retrievers independently | packages/eoip/gaps/enterprise_completion.py:47 | tests/unit/test_enterprise_gap_completion.py:40 |
| gap-coverage-audit.json | GAP-RET-006 | P0 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 21. Unified Retrieval Fabric / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:668 | GAP-RET-006: Provide retrieval trace for debugging | packages/eoip/contracts/retrieval.py:28, packages/eoip/gaps/enterprise_completion.py:47, packages/eoip/retrieval/service.py:324 | tests/unit/test_enterprise_gap_completion.py:40 |
| gap-coverage-audit.json | GAP-SEARCH-001 | P1 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 4. Competitive Study / 4.3 Ontotext GraphDB / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:168 | GAP-SEARCH-001: Add synchronized full-text + vector + graph hybrid search with freshness guarantees | packages/eoip/models/embeddings.py:1, packages/eoip/models/embeddings.py:28, packages/eoip/models/embeddings.py:120 | tests/unit/test_embeddings.py:1, tests/unit/test_extended_api_routes_pass2.py:5, tests/unit/test_search_facets.py:1 |
| gap-coverage-audit.json | GAP-SEARCH-002 | P1 | done | 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 4. Competitive Study / 4.3 Ontotext GraphDB / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:169 | GAP-SEARCH-002: Search results must preserve graph identity and provenance | packages/eoip/retrieval/vectors.py:4, packages/eoip/retrieval/vectors.py:294, packages/eoip/search/facets.py:5 | tests/unit/test_search_facets.py:1, tests/unit/test_search_facets.py:116 |
| g2-coverage-audit.json | G2-GRAPH-OBS-001 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 9.2 Observability Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:886 | G2-GRAPH-OBS-001 | packages/eoip/gaps/g2_readiness.py:18, packages/eoip/gaps/g2_readiness.py:183 | tests/unit/test_g2_readiness.py:15 |
| g2-coverage-audit.json | G2-GRAPH-OBS-002 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 9.2 Observability Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:899 | G2-GRAPH-OBS-002 | packages/eoip/gaps/g2_readiness.py:18, packages/eoip/gaps/g2_readiness.py:183 | tests/unit/test_g2_readiness.py:15 |
| g2-coverage-audit.json | G2-GRAPH-OBS-003 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 9.2 Observability Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:902 | G2-GRAPH-OBS-003 | packages/eoip/gaps/g2_readiness.py:18, packages/eoip/gaps/g2_readiness.py:183 | tests/unit/test_g2_readiness.py:15 |
| g2-coverage-audit.json | G2-GRAPH-RUNTIME-001 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 9.3 Runtime Topology Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:909 | G2-GRAPH-RUNTIME-001 | packages/eoip/gaps/g2_readiness.py:20, packages/eoip/gaps/g2_readiness.py:184 | tests/unit/test_g2_readiness.py:17 |
| g2-coverage-audit.json | G2-GRAPH-RUNTIME-002 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 9.3 Runtime Topology Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:912 | G2-GRAPH-RUNTIME-002 | packages/eoip/gaps/g2_readiness.py:20, packages/eoip/gaps/g2_readiness.py:184 | tests/unit/test_g2_readiness.py:17 |
| g2-coverage-audit.json | G2-GRAPH-RUNTIME-003 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 9.3 Runtime Topology Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:915 | G2-GRAPH-RUNTIME-003 | packages/eoip/gaps/g2_readiness.py:20, packages/eoip/gaps/g2_readiness.py:184 | tests/unit/test_g2_readiness.py:17 |
| g2-coverage-audit.json | G2-GRAPH-SEC-001 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 9.4 Security & Supply-Chain Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:922 | G2-GRAPH-SEC-001 | packages/eoip/gaps/g2_readiness.py:21, packages/eoip/gaps/g2_readiness.py:185 | tests/unit/test_g2_readiness.py:18 |
| g2-coverage-audit.json | G2-GRAPH-SEC-002 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 9.4 Security & Supply-Chain Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:925 | G2-GRAPH-SEC-002 | packages/eoip/gaps/g2_readiness.py:21, packages/eoip/gaps/g2_readiness.py:185 | tests/unit/test_g2_readiness.py:18 |
| g2-coverage-audit.json | G2-GRAPH-SEC-003 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 9.4 Security & Supply-Chain Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:928 | G2-GRAPH-SEC-003 | packages/eoip/gaps/g2_readiness.py:21, packages/eoip/gaps/g2_readiness.py:185 | tests/unit/test_g2_readiness.py:18 |
| g2-coverage-audit.json | G2-SRC-CICD-001 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.13 CI/CD | EOIP-engg-doc-pkg/gaps2-requirements.md:575 | G2-SRC-CICD-001 | packages/eoip/connectors/cicd.py:1, packages/eoip/connectors/cicd.py:22, packages/eoip/gaps/g2_readiness.py:37 | tests/unit/test_g2_readiness.py:34 |
| g2-coverage-audit.json | G2-SRC-CICD-002 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.13 CI/CD | EOIP-engg-doc-pkg/gaps2-requirements.md:578 | G2-SRC-CICD-002 | packages/eoip/connectors/cicd.py:1, packages/eoip/connectors/cicd.py:22, packages/eoip/gaps/g2_readiness.py:37 | tests/unit/test_g2_readiness.py:34 |
| g2-coverage-audit.json | G2-SRC-CICD-003 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.13 CI/CD | EOIP-engg-doc-pkg/gaps2-requirements.md:582 | G2-SRC-CICD-003 | packages/eoip/connectors/cicd.py:1, packages/eoip/connectors/cicd.py:22, packages/eoip/gaps/g2_readiness.py:37 | tests/unit/test_g2_readiness.py:34 |
| g2-coverage-audit.json | G2-SRC-CICD-004 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.13 CI/CD | EOIP-engg-doc-pkg/gaps2-requirements.md:585 | G2-SRC-CICD-004 | packages/eoip/connectors/cicd.py:1, packages/eoip/connectors/cicd.py:22, packages/eoip/gaps/g2_readiness.py:37 | tests/unit/test_g2_readiness.py:34 |
| g2-coverage-audit.json | G2-SRC-DD-001 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.10 Datadog | EOIP-engg-doc-pkg/gaps2-requirements.md:526 | G2-SRC-DD-001 | packages/eoip/gaps/g2_readiness.py:40, packages/eoip/gaps/g2_readiness.py:154 | tests/unit/test_g2_readiness.py:37 |
| g2-coverage-audit.json | G2-SRC-DD-002 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.10 Datadog | EOIP-engg-doc-pkg/gaps2-requirements.md:529 | G2-SRC-DD-002 | packages/eoip/gaps/g2_readiness.py:40, packages/eoip/gaps/g2_readiness.py:154 | tests/unit/test_g2_readiness.py:37 |
| g2-coverage-audit.json | G2-SRC-DD-003 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.10 Datadog | EOIP-engg-doc-pkg/gaps2-requirements.md:532 | G2-SRC-DD-003 | packages/eoip/gaps/g2_readiness.py:40, packages/eoip/gaps/g2_readiness.py:154 | tests/unit/test_g2_readiness.py:37 |
| g2-coverage-audit.json | G2-SRC-DD-004 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.10 Datadog | EOIP-engg-doc-pkg/gaps2-requirements.md:535 | G2-SRC-DD-004 | packages/eoip/gaps/g2_readiness.py:40, packages/eoip/gaps/g2_readiness.py:154 | tests/unit/test_g2_readiness.py:37 |
| g2-coverage-audit.json | G2-SRC-GRAF-001 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.11 Grafana | EOIP-engg-doc-pkg/gaps2-requirements.md:542 | G2-SRC-GRAF-001 | packages/eoip/gaps/g2_readiness.py:43, packages/eoip/gaps/g2_readiness.py:155 | tests/unit/test_g2_readiness.py:40 |
| g2-coverage-audit.json | G2-SRC-GRAF-002 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.11 Grafana | EOIP-engg-doc-pkg/gaps2-requirements.md:545 | G2-SRC-GRAF-002 | packages/eoip/gaps/g2_readiness.py:43, packages/eoip/gaps/g2_readiness.py:155 | tests/unit/test_g2_readiness.py:40 |
| g2-coverage-audit.json | G2-SRC-GRAF-003 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.11 Grafana | EOIP-engg-doc-pkg/gaps2-requirements.md:549 | G2-SRC-GRAF-003 | packages/eoip/gaps/g2_readiness.py:43, packages/eoip/gaps/g2_readiness.py:155 | tests/unit/test_g2_readiness.py:40 |
| g2-coverage-audit.json | G2-SRC-KIB-001 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.9 Kibana / Elastic Observability | EOIP-engg-doc-pkg/gaps2-requirements.md:500 | G2-SRC-KIB-001 | packages/eoip/gaps/g2_readiness.py:45, packages/eoip/gaps/g2_readiness.py:153 | tests/unit/test_g2_readiness.py:42 |
| g2-coverage-audit.json | G2-SRC-KIB-002 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.9 Kibana / Elastic Observability | EOIP-engg-doc-pkg/gaps2-requirements.md:503 | G2-SRC-KIB-002 | packages/eoip/gaps/g2_readiness.py:45, packages/eoip/gaps/g2_readiness.py:153 | tests/unit/test_g2_readiness.py:42 |
| g2-coverage-audit.json | G2-SRC-KIB-003 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.9 Kibana / Elastic Observability | EOIP-engg-doc-pkg/gaps2-requirements.md:506 | G2-SRC-KIB-003 | packages/eoip/gaps/g2_readiness.py:45, packages/eoip/gaps/g2_readiness.py:153 | tests/unit/test_g2_readiness.py:42 |
| g2-coverage-audit.json | G2-SRC-KIB-004 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.9 Kibana / Elastic Observability | EOIP-engg-doc-pkg/gaps2-requirements.md:509 | G2-SRC-KIB-004 | packages/eoip/gaps/g2_readiness.py:45, packages/eoip/gaps/g2_readiness.py:153 | tests/unit/test_g2_readiness.py:42 |
| g2-coverage-audit.json | G2-SRC-KIB-005 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.9 Kibana / Elastic Observability | EOIP-engg-doc-pkg/gaps2-requirements.md:519 | G2-SRC-KIB-005 | packages/eoip/gaps/g2_readiness.py:45, packages/eoip/gaps/g2_readiness.py:153 | tests/unit/test_g2_readiness.py:42 |
| g2-coverage-audit.json | G2-SRC-OTEL-001 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.12 OpenTelemetry | EOIP-engg-doc-pkg/gaps2-requirements.md:556 | G2-SRC-OTEL-001 | packages/eoip/connectors/otel.py:1, packages/eoip/connectors/otel.py:32, packages/eoip/gaps/g2_readiness.py:46 | tests/unit/test_g2_readiness.py:43 |
| g2-coverage-audit.json | G2-SRC-OTEL-002 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.12 OpenTelemetry | EOIP-engg-doc-pkg/gaps2-requirements.md:559 | G2-SRC-OTEL-002 | packages/eoip/connectors/otel.py:1, packages/eoip/connectors/otel.py:32, packages/eoip/gaps/g2_readiness.py:46 | tests/unit/test_g2_readiness.py:43 |
| g2-coverage-audit.json | G2-SRC-OTEL-003 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.12 OpenTelemetry | EOIP-engg-doc-pkg/gaps2-requirements.md:562 | G2-SRC-OTEL-003 | packages/eoip/connectors/otel.py:1, packages/eoip/connectors/otel.py:32, packages/eoip/gaps/g2_readiness.py:46 | tests/unit/test_g2_readiness.py:43 |
| g2-coverage-audit.json | G2-SRC-OTEL-004 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.12 OpenTelemetry | EOIP-engg-doc-pkg/gaps2-requirements.md:565 | G2-SRC-OTEL-004 | packages/eoip/connectors/otel.py:1, packages/eoip/connectors/otel.py:32, packages/eoip/gaps/g2_readiness.py:46 | tests/unit/test_g2_readiness.py:43 |
| g2-coverage-audit.json | G2-SRC-OTEL-005 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.12 OpenTelemetry | EOIP-engg-doc-pkg/gaps2-requirements.md:568 | G2-SRC-OTEL-005 | packages/eoip/connectors/otel.py:1, packages/eoip/connectors/otel.py:32, packages/eoip/gaps/g2_readiness.py:46 | tests/unit/test_g2_readiness.py:43 |
| g2-coverage-audit.json | G2-SRC-RUNTIME-001 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.14 Docker / Kubernetes / Runtime Infrastructure | EOIP-engg-doc-pkg/gaps2-requirements.md:592 | G2-SRC-RUNTIME-001 | packages/eoip/connectors/runtime_infra.py:1, packages/eoip/connectors/runtime_infra.py:31, packages/eoip/gaps/g2_readiness.py:47 | tests/unit/test_g2_readiness.py:44 |
| g2-coverage-audit.json | G2-SRC-RUNTIME-002 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.14 Docker / Kubernetes / Runtime Infrastructure | EOIP-engg-doc-pkg/gaps2-requirements.md:595 | G2-SRC-RUNTIME-002 | packages/eoip/connectors/runtime_infra.py:1, packages/eoip/connectors/runtime_infra.py:31, packages/eoip/gaps/g2_readiness.py:47 | tests/unit/test_g2_readiness.py:44 |
| g2-coverage-audit.json | G2-SRC-RUNTIME-003 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.14 Docker / Kubernetes / Runtime Infrastructure | EOIP-engg-doc-pkg/gaps2-requirements.md:598 | G2-SRC-RUNTIME-003 | packages/eoip/connectors/runtime_infra.py:1, packages/eoip/connectors/runtime_infra.py:31, packages/eoip/gaps/g2_readiness.py:47 | tests/unit/test_g2_readiness.py:44 |
| g2-coverage-audit.json | G2-SRC-SBOM-001 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.15 SBOM / SCA / Vulnerability | EOIP-engg-doc-pkg/gaps2-requirements.md:605 | G2-SRC-SBOM-001 | packages/eoip/connectors/sbom.py:1, packages/eoip/connectors/sbom.py:23, packages/eoip/gaps/g2_readiness.py:48 | tests/unit/test_g2_readiness.py:45 |
| g2-coverage-audit.json | G2-SRC-SBOM-002 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.15 SBOM / SCA / Vulnerability | EOIP-engg-doc-pkg/gaps2-requirements.md:608 | G2-SRC-SBOM-002 | packages/eoip/connectors/sbom.py:1, packages/eoip/connectors/sbom.py:23, packages/eoip/gaps/g2_readiness.py:48 | tests/unit/test_g2_readiness.py:45 |
| g2-coverage-audit.json | G2-SRC-SBOM-003 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.15 SBOM / SCA / Vulnerability | EOIP-engg-doc-pkg/gaps2-requirements.md:612 | G2-SRC-SBOM-003 | packages/eoip/connectors/sbom.py:1, packages/eoip/connectors/sbom.py:23, packages/eoip/gaps/g2_readiness.py:48 | tests/unit/test_g2_readiness.py:45 |
| g2-coverage-audit.json | G2-SRC-SBOM-004 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 4.15 SBOM / SCA / Vulnerability | EOIP-engg-doc-pkg/gaps2-requirements.md:615 | G2-SRC-SBOM-004 | packages/eoip/connectors/sbom.py:1, packages/eoip/connectors/sbom.py:23, packages/eoip/gaps/g2_readiness.py:48 | tests/unit/test_g2_readiness.py:45, tests/unit/test_g2_readiness.py:101 |
| g2-coverage-audit.json | G2-TEL-001 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 28. Telemetry Semantics and Storage Rules | EOIP-engg-doc-pkg/gaps2-requirements.md:1634 | G2-TEL-001 | packages/eoip/gaps/g2_readiness.py:53, packages/eoip/gaps/g2_readiness.py:260 | tests/unit/test_g2_readiness.py:50 |
| g2-coverage-audit.json | G2-TEL-002 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 28. Telemetry Semantics and Storage Rules | EOIP-engg-doc-pkg/gaps2-requirements.md:1637 | G2-TEL-002 | packages/eoip/gaps/g2_readiness.py:53, packages/eoip/gaps/g2_readiness.py:260 | tests/unit/test_g2_readiness.py:50 |
| g2-coverage-audit.json | G2-TEL-003 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 28. Telemetry Semantics and Storage Rules | EOIP-engg-doc-pkg/gaps2-requirements.md:1640 | G2-TEL-003 | packages/eoip/gaps/g2_readiness.py:53, packages/eoip/gaps/g2_readiness.py:260 | tests/unit/test_g2_readiness.py:50 |
| g2-coverage-audit.json | G2-TEL-004 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 28. Telemetry Semantics and Storage Rules | EOIP-engg-doc-pkg/gaps2-requirements.md:1643 | G2-TEL-004 | packages/eoip/gaps/g2_readiness.py:53, packages/eoip/gaps/g2_readiness.py:260 | tests/unit/test_g2_readiness.py:50 |
| g2-coverage-audit.json | G2-TEL-005 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 28. Telemetry Semantics and Storage Rules | EOIP-engg-doc-pkg/gaps2-requirements.md:1646 | G2-TEL-005 | packages/eoip/gaps/g2_readiness.py:53, packages/eoip/gaps/g2_readiness.py:260 | tests/unit/test_g2_readiness.py:50 |
| g2-coverage-audit.json | G2-TEL-006 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 28. Telemetry Semantics and Storage Rules | EOIP-engg-doc-pkg/gaps2-requirements.md:1649 | G2-TEL-006 | packages/eoip/gaps/g2_readiness.py:53, packages/eoip/gaps/g2_readiness.py:260 | tests/unit/test_g2_readiness.py:50 |
| g2-coverage-audit.json | G2-TEL-007 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 28. Telemetry Semantics and Storage Rules | EOIP-engg-doc-pkg/gaps2-requirements.md:1652 | G2-TEL-007 | packages/eoip/gaps/g2_readiness.py:53, packages/eoip/gaps/g2_readiness.py:260 | tests/unit/test_g2_readiness.py:50 |
| g2-coverage-audit.json | G2-TEL-008 | P2 | done | 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 28. Telemetry Semantics and Storage Rules | EOIP-engg-doc-pkg/gaps2-requirements.md:1655 | G2-TEL-008 | packages/eoip/gaps/g2_readiness.py:53, packages/eoip/gaps/g2_readiness.py:260 | tests/unit/test_g2_readiness.py:50 |
| gap-coverage-audit.json | GAP-CATALOG-001 | P0 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 4. Competitive Study / 4.8 data.world / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:296 | GAP-CATALOG-001: Add an enterprise Knowledge Catalog over all graph assets | packages/eoip/future_scope.py:20, packages/eoip/future_scope.py:55, packages/eoip/future_scope.py:513 | tests/unit/test_enterprise_gap_completion.py:10 |
| gap-coverage-audit.json | GAP-CATALOG-002 | P0 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 4. Competitive Study / 4.8 data.world / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:297 | GAP-CATALOG-002: Support asset certification states: Draft, Candidate, Trusted, Certified, Deprecated, Quarantined | packages/eoip/future_scope.py:20, packages/eoip/future_scope.py:56, packages/eoip/future_scope.py:513 | tests/unit/test_enterprise_gap_completion.py:10 |
| gap-coverage-audit.json | GAP-CATALOG-003 | P0 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 4. Competitive Study / 4.8 data.world / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:298 | GAP-CATALOG-003: Create stewardship assignments and data/knowledge ownership | packages/eoip/future_scope.py:20, packages/eoip/future_scope.py:57, packages/eoip/future_scope.py:513 | tests/unit/test_enterprise_gap_completion.py:10 |
| gap-coverage-audit.json | GAP-CATALOG-004 | P0 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 4. Competitive Study / 4.8 data.world / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:299 | GAP-CATALOG-004: Add domain collections / knowledge products | packages/eoip/future_scope.py:20, packages/eoip/future_scope.py:58, packages/eoip/future_scope.py:513 | tests/unit/test_enterprise_gap_completion.py:10 |
| gap-coverage-audit.json | GAP-CATALOG-005 | P0 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 4. Competitive Study / 4.8 data.world / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:300 | GAP-CATALOG-005: Provide lineage-impact navigation from catalog to underlying graph path | packages/eoip/future_scope.py:20, packages/eoip/future_scope.py:59, packages/eoip/future_scope.py:513 | tests/unit/test_future_scope.py:38 |
| gap-coverage-audit.json | GAP-DATAOPS-001 | P2 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 4. Competitive Study / 4.6 Cambridge Semantics Anzo / Graph Studio / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:255 | GAP-DATAOPS-001: Capture every transformation as lineage metadata | packages/eoip/future_scope.py:18, packages/eoip/future_scope.py:51, packages/eoip/future_scope.py:423 | tests/unit/test_enterprise_gap_completion.py:16 |
| gap-coverage-audit.json | GAP-FABRIC-001 | P1 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 20. Federated Knowledge Fabric / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:638 | GAP-FABRIC-001: Query materialized HugeGraph data and selected external sources in one plan | packages/eoip/federation/planner.py:1, packages/eoip/federation/planner.py:27, packages/eoip/federation/planner.py:36 | tests/unit/test_federation_planner.py:1 |
| gap-coverage-audit.json | GAP-FABRIC-002 | P1 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 20. Federated Knowledge Fabric / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:639 | GAP-FABRIC-002: Source capability registry | packages/eoip/federation/planner.py:1, packages/eoip/federation/planner.py:55, packages/eoip/federation/planner.py:245 | tests/unit/test_federation_planner.py:1 |
| gap-coverage-audit.json | GAP-FABRIC-003 | P1 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 20. Federated Knowledge Fabric / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:640 | GAP-FABRIC-003: Cost-aware query routing | packages/eoip/federation/planner.py:1, packages/eoip/federation/planner.py:7, packages/eoip/federation/planner.py:245 | tests/unit/test_federation_planner.py:1 |
| gap-coverage-audit.json | GAP-FABRIC-004 | P1 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 20. Federated Knowledge Fabric / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:641 | GAP-FABRIC-004: Push filters/projections to source where possible | packages/eoip/federation/planner.py:1, packages/eoip/federation/planner.py:5, packages/eoip/federation/planner.py:245 | tests/unit/test_federation_planner.py:1 |
| gap-coverage-audit.json | GAP-FABRIC-005 | P1 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 20. Federated Knowledge Fabric / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:642 | GAP-FABRIC-005: Local result cache with provenance/freshness | packages/eoip/federation/planner.py:1, packages/eoip/federation/planner.py:6, packages/eoip/federation/planner.py:245 | tests/unit/test_federation_planner.py:1 |
| gap-coverage-audit.json | GAP-FABRIC-006 | P1 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 20. Federated Knowledge Fabric / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:643 | GAP-FABRIC-006: Offline degradation strategy | packages/eoip/federation/planner.py:1, packages/eoip/federation/planner.py:8, packages/eoip/federation/planner.py:245 | tests/unit/test_federation_planner.py:1 |
| gap-coverage-audit.json | GAP-FABRIC-007 | P1 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 20. Federated Knowledge Fabric / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:644 | GAP-FABRIC-007: Explain query routing | packages/eoip/federation/planner.py:1, packages/eoip/federation/planner.py:9, packages/eoip/federation/planner.py:119 | tests/unit/test_federation_planner.py:1 |
| gap-coverage-audit.json | GAP-FABRIC-008 | P1 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 20. Federated Knowledge Fabric / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:645 | GAP-FABRIC-008: Enforce source-level data policies | packages/eoip/federation/planner.py:1, packages/eoip/federation/planner.py:245, packages/eoip/federation/__init__.py:1 | tests/unit/test_federation_planner.py:1 |
| gap-coverage-audit.json | GAP-FED-001 | P1 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 4. Competitive Study / 4.1 Stardog / Requirements to turn these trade-offs into strengths | EOIP-engg-doc-pkg/gaps-requirements.md:117 | GAP-FED-001: Build a first-class Semantic Federation & Virtualization Layer for external sources without forcing materialization | packages/eoip/future_scope.py:10, packages/eoip/future_scope.py:36, packages/eoip/future_scope.py:111 | tests/unit/test_enterprise_gap_completion.py:22 |
| gap-coverage-audit.json | GAP-FED-002 | P1 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 4. Competitive Study / 4.1 Stardog / Requirements to turn these trade-offs into strengths | EOIP-engg-doc-pkg/gaps-requirements.md:118 | GAP-FED-002: Support policy-controlled choice between VIRTUAL, CACHE, MATERIALIZE, and HYBRID per source/entity type | packages/eoip/future_scope.py:10, packages/eoip/future_scope.py:37, packages/eoip/future_scope.py:93 | tests/unit/test_enterprise_gap_completion.py:22 |
| gap-coverage-audit.json | GAP-FED-003 | P1 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 4. Competitive Study / 4.1 Stardog / Requirements to turn these trade-offs into strengths | EOIP-engg-doc-pkg/gaps-requirements.md:119 | GAP-FED-003: Maintain explainable query plans showing which results came from HugeGraph versus live sources | packages/eoip/future_scope.py:10, packages/eoip/future_scope.py:38, packages/eoip/future_scope.py:111 | tests/unit/test_enterprise_gap_completion.py:22 |
| gap-coverage-audit.json | GAP-FED-004 | P1 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 4. Competitive Study / 4.1 Stardog / Requirements to turn these trade-offs into strengths | EOIP-engg-doc-pkg/gaps-requirements.md:120 | GAP-FED-004: Build federation adapters independently of HugeGraph so the product can query JDBC/REST/file sources while keeping HugeGraph as semantic control pl | packages/eoip/future_scope.py:10, packages/eoip/future_scope.py:39, packages/eoip/future_scope.py:111 | tests/unit/test_future_scope.py:37 |
| gap-coverage-audit.json | GAP-KP-001 | P1 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 17. Knowledge Catalog & Knowledge Products / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:581 | GAP-KP-001: Catalog every graph, ontology, data source, connector, model, query, agent and knowledge product | packages/eoip/catalog/products.py:1, packages/eoip/catalog/products.py:64, packages/eoip/catalog/products.py:161 | tests/unit/test_knowledge_products.py:1, tests/unit/test_knowledge_products.py:45 |
| gap-coverage-audit.json | GAP-KP-002 | P1 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 17. Knowledge Catalog & Knowledge Products / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:582 | GAP-KP-002: A Knowledge Product defines: | packages/eoip/catalog/products.py:1, packages/eoip/catalog/products.py:27, packages/eoip/catalog/products.py:36 | tests/unit/test_knowledge_products.py:1, tests/unit/test_knowledge_products.py:98 |
| gap-coverage-audit.json | GAP-KP-003 | P1 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 17. Knowledge Catalog & Knowledge Products / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:593 | GAP-KP-003: Product states: Draft, Experimental, Trusted, Certified, Deprecated | packages/eoip/catalog/products.py:1, packages/eoip/catalog/products.py:161, packages/eoip/catalog/products.py:219 | tests/unit/test_knowledge_products.py:1, tests/unit/test_knowledge_products.py:132 |
| gap-coverage-audit.json | GAP-KP-004 | P1 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 17. Knowledge Catalog & Knowledge Products / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:594 | GAP-KP-004: Product lineage must be navigable | packages/eoip/catalog/products.py:1, packages/eoip/catalog/products.py:161, packages/eoip/catalog/products.py:261 | tests/unit/test_knowledge_products.py:1, tests/unit/test_knowledge_products.py:169 |
| gap-coverage-audit.json | GAP-KP-005 | P1 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 17. Knowledge Catalog & Knowledge Products / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:595 | GAP-KP-005: Export/import product definitions | packages/eoip/catalog/products.py:1, packages/eoip/catalog/products.py:161, packages/eoip/catalog/products.py:296 | tests/unit/test_knowledge_products.py:1, tests/unit/test_knowledge_products.py:203 |
| gap-coverage-audit.json | GAP-LAYER-001 | P2 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 4. Competitive Study / 4.6 Cambridge Semantics Anzo / Graph Studio / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:245 | GAP-LAYER-001: Introduce Graph Views / Knowledge Products comparable conceptually to curated graph subsets: | packages/eoip/future_scope.py:16, packages/eoip/future_scope.py:46, packages/eoip/future_scope.py:352 | tests/unit/test_enterprise_gap_completion.py:31 |
| gap-coverage-audit.json | GAP-LAYER-002 | P2 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 4. Competitive Study / 4.6 Cambridge Semantics Anzo / Graph Studio / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:252 | GAP-LAYER-002: Views must be declarative, versioned and reproducible | packages/eoip/future_scope.py:16, packages/eoip/future_scope.py:47, packages/eoip/future_scope.py:352 | tests/unit/test_enterprise_gap_completion.py:31 |
| gap-coverage-audit.json | GAP-LIN-001 | P2 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 28. Data & Knowledge Lineage Interoperability / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:791 | GAP-LIN-001: Map internal lineage to OpenLineage concepts where applicable | packages/eoip/future_scope.py:60, packages/eoip/future_scope.py:587, packages/eoip/gaps/enterprise_completion.py:40 | tests/unit/test_enterprise_gap_completion.py:33 |
| gap-coverage-audit.json | GAP-LIN-002 | P2 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 28. Data & Knowledge Lineage Interoperability / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:792 | GAP-LIN-002: Map semantic provenance to PROV-O where applicable | packages/eoip/future_scope.py:61, packages/eoip/future_scope.py:587, packages/eoip/gaps/enterprise_completion.py:40 | tests/unit/test_enterprise_gap_completion.py:33 |
| gap-coverage-audit.json | GAP-LIN-003 | P2 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 28. Data & Knowledge Lineage Interoperability / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:793 | GAP-LIN-003: Keep internal richer model without losing standards compatibility | packages/eoip/future_scope.py:62, packages/eoip/future_scope.py:587, packages/eoip/gaps/enterprise_completion.py:40 | tests/unit/test_enterprise_gap_completion.py:33 |
| gap-coverage-audit.json | GAP-LIN-004 | P2 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 28. Data & Knowledge Lineage Interoperability / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:794 | GAP-LIN-004: Ingest lineage events from CI/CD and data pipelines | packages/eoip/future_scope.py:63, packages/eoip/future_scope.py:587, packages/eoip/gaps/enterprise_completion.py:40 | tests/unit/test_enterprise_gap_completion.py:33 |
| gap-coverage-audit.json | GAP-LIN-005 | P2 | done | 8. Phase 5 — Federation, Catalog & Knowledge Products | 28. Data & Knowledge Lineage Interoperability / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:795 | GAP-LIN-005: Emit lineage events for platform transformations | packages/eoip/future_scope.py:64, packages/eoip/future_scope.py:587, packages/eoip/gaps/enterprise_completion.py:40 | tests/unit/test_enterprise_gap_completion.py:33 |
| g2-coverage-audit.json | G2-I2R-001 | P2 | done | 9. G2-P6 — Expanded Semantic Digital Twin | 20. Intent-to-Runtime Traceability | EOIP-engg-doc-pkg/gaps2-requirements.md:1348 | G2-I2R-001 | packages/eoip/gaps/g2_readiness.py:23, packages/eoip/gaps/g2_readiness.py:230 | tests/unit/test_g2_readiness.py:20 |
| g2-coverage-audit.json | G2-I2R-002 | P2 | done | 9. G2-P6 — Expanded Semantic Digital Twin | 20. Intent-to-Runtime Traceability | EOIP-engg-doc-pkg/gaps2-requirements.md:1352 | G2-I2R-002 | packages/eoip/gaps/g2_readiness.py:23, packages/eoip/gaps/g2_readiness.py:230 | tests/unit/test_g2_readiness.py:20 |
| g2-coverage-audit.json | G2-I2R-003 | P2 | done | 9. G2-P6 — Expanded Semantic Digital Twin | 20. Intent-to-Runtime Traceability | EOIP-engg-doc-pkg/gaps2-requirements.md:1355 | G2-I2R-003 | packages/eoip/gaps/g2_readiness.py:23, packages/eoip/gaps/g2_readiness.py:230 | tests/unit/test_g2_readiness.py:20 |
| g2-coverage-audit.json | G2-I2R-004 | P2 | done | 9. G2-P6 — Expanded Semantic Digital Twin | 20. Intent-to-Runtime Traceability | EOIP-engg-doc-pkg/gaps2-requirements.md:1358 | G2-I2R-004 | packages/eoip/gaps/g2_readiness.py:23, packages/eoip/gaps/g2_readiness.py:230 | tests/unit/test_g2_readiness.py:20 |
| g2-coverage-audit.json | G2-I2R-005 | P2 | done | 9. G2-P6 — Expanded Semantic Digital Twin | 20. Intent-to-Runtime Traceability | EOIP-engg-doc-pkg/gaps2-requirements.md:1361 | G2-I2R-005 | packages/eoip/gaps/g2_readiness.py:23, packages/eoip/gaps/g2_readiness.py:230 | tests/unit/test_g2_readiness.py:20 |
| g2-coverage-audit.json | G2-TWIN-001 | P2 | done | 9. G2-P6 — Expanded Semantic Digital Twin | 10. Live Enterprise Digital Knowledge Twin | EOIP-engg-doc-pkg/gaps2-requirements.md:1005 | G2-TWIN-001 | packages/eoip/gaps/g2_readiness.py:55, packages/eoip/gaps/g2_readiness.py:190, packages/eoip/graph/twin.py:1 | tests/unit/test_g2_readiness.py:52 |
| g2-coverage-audit.json | G2-TWIN-002 | P2 | done | 9. G2-P6 — Expanded Semantic Digital Twin | 10. Live Enterprise Digital Knowledge Twin | EOIP-engg-doc-pkg/gaps2-requirements.md:1008 | G2-TWIN-002 | packages/eoip/gaps/g2_readiness.py:55, packages/eoip/gaps/g2_readiness.py:190, packages/eoip/graph/twin.py:1 | tests/unit/test_g2_readiness.py:52 |
| g2-coverage-audit.json | G2-TWIN-003 | P2 | done | 9. G2-P6 — Expanded Semantic Digital Twin | 10. Live Enterprise Digital Knowledge Twin | EOIP-engg-doc-pkg/gaps2-requirements.md:1025 | G2-TWIN-003 | packages/eoip/gaps/g2_readiness.py:55, packages/eoip/gaps/g2_readiness.py:190, packages/eoip/graph/twin.py:1 | tests/unit/test_g2_readiness.py:52 |
| g2-coverage-audit.json | G2-TWIN-004 | P2 | done | 9. G2-P6 — Expanded Semantic Digital Twin | 10. Live Enterprise Digital Knowledge Twin | EOIP-engg-doc-pkg/gaps2-requirements.md:1028 | G2-TWIN-004 | packages/eoip/gaps/g2_readiness.py:55, packages/eoip/gaps/g2_readiness.py:190, packages/eoip/graph/twin.py:1 | tests/unit/test_g2_readiness.py:52 |
| g2-coverage-audit.json | G2-TWIN-005 | P2 | done | 9. G2-P6 — Expanded Semantic Digital Twin | 10. Live Enterprise Digital Knowledge Twin | EOIP-engg-doc-pkg/gaps2-requirements.md:1031 | G2-TWIN-005 | packages/eoip/gaps/g2_readiness.py:55, packages/eoip/gaps/g2_readiness.py:190, packages/eoip/graph/twin.py:1 | tests/unit/test_g2_readiness.py:52 |
| gap-coverage-audit.json | GAP-AGOV-005 | P0 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 24. Agent & MCP Governance / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:718 | GAP-AGOV-005: Per-agent time/step/tool/model budgets | packages/eoip/gaps/enterprise_completion.py:11 | tests/unit/test_enterprise_gap_completion.py:4 |
| gap-coverage-audit.json | GAP-AGOV-006 | P0 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 24. Agent & MCP Governance / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:719 | GAP-AGOV-006: Prompt-injection detection | packages/eoip/agents/firewall.py:12 | tests/unit/test_gap_governance_controls.py:12, tests/unit/test_gap_governance_controls.py:57 |
| gap-coverage-audit.json | GAP-AGOV-007 | P0 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 24. Agent & MCP Governance / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:720 | GAP-AGOV-007: Tool-output sanitization | packages/eoip/agents/firewall.py:13 | tests/unit/test_gap_governance_controls.py:13, tests/unit/test_gap_governance_controls.py:58 |
| gap-coverage-audit.json | GAP-AGOV-008 | P0 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 24. Agent & MCP Governance / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:721 | GAP-AGOV-008: MCP server allowlist | packages/eoip/gaps/enterprise_completion.py:12 | tests/unit/test_enterprise_gap_completion.py:5 |
| gap-coverage-audit.json | GAP-AGOV-009 | P0 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 24. Agent & MCP Governance / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:722 | GAP-AGOV-009: Complete action provenance | packages/eoip/gaps/enterprise_completion.py:12 | tests/unit/test_enterprise_gap_completion.py:5 |
| gap-coverage-audit.json | GAP-AGOV-010 | P0 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 24. Agent & MCP Governance / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:723 | GAP-AGOV-010: Replayable agent execution traces excluding private chain-of-thought | packages/eoip/gaps/enterprise_completion.py:12 | tests/unit/test_enterprise_gap_completion.py:5 |
| gap-coverage-audit.json | GAP-AGOV-011 | P0 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 24. Agent & MCP Governance / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:724 | GAP-AGOV-011: Deterministic dry-run mode | packages/eoip/gaps/enterprise_completion.py:12 | tests/unit/test_enterprise_gap_completion.py:5 |
| gap-coverage-audit.json | GAP-AGOV-012 | P0 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 24. Agent & MCP Governance / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:725 | GAP-AGOV-012: Agent evaluation gates before promotion | packages/eoip/models/governance.py:1, packages/eoip/models/governance.py:6, packages/eoip/models/governance.py:43 | tests/unit/test_model_governance.py:1 |
| gap-coverage-audit.json | GAP-AKO-001 | P2 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 23. Agentic Knowledge Operations / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:695 | GAP-AKO-001: Knowledge Curator Agent | packages/eoip/gaps/enterprise_completion.py:13 | tests/unit/test_enterprise_gap_completion.py:6 |
| gap-coverage-audit.json | GAP-AKO-002 | P2 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 23. Agentic Knowledge Operations / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:696 | GAP-AKO-002: Ontology Reviewer Agent | packages/eoip/gaps/enterprise_completion.py:13 | tests/unit/test_enterprise_gap_completion.py:6 |
| gap-coverage-audit.json | GAP-AKO-003 | P2 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 23. Agentic Knowledge Operations / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:697 | GAP-AKO-003: Data Quality Agent | packages/eoip/gaps/enterprise_completion.py:13 | tests/unit/test_enterprise_gap_completion.py:6 |
| gap-coverage-audit.json | GAP-AKO-004 | P2 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 23. Agentic Knowledge Operations / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:698 | GAP-AKO-004: Connector Diagnosis Agent | packages/eoip/gaps/enterprise_completion.py:13 | tests/unit/test_enterprise_gap_completion.py:6 |
| gap-coverage-audit.json | GAP-AKO-005 | P2 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 23. Agentic Knowledge Operations / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:699 | GAP-AKO-005: Change Impact Agent | packages/eoip/gaps/enterprise_completion.py:13 | tests/unit/test_enterprise_gap_completion.py:6 |
| gap-coverage-audit.json | GAP-AKO-006 | P2 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 23. Agentic Knowledge Operations / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:700 | GAP-AKO-006: Architecture Conformance Agent | packages/eoip/gaps/enterprise_completion.py:13 | tests/unit/test_enterprise_gap_completion.py:6 |
| gap-coverage-audit.json | GAP-AKO-007 | P2 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 23. Agentic Knowledge Operations / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:701 | GAP-AKO-007: Incident Investigation Agent | packages/eoip/gaps/enterprise_completion.py:14 | tests/unit/test_enterprise_gap_completion.py:7 |
| gap-coverage-audit.json | GAP-AKO-008 | P2 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 23. Agentic Knowledge Operations / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:702 | GAP-AKO-008: Documentation Freshness Agent | packages/eoip/gaps/enterprise_completion.py:14 | tests/unit/test_enterprise_gap_completion.py:7 |
| gap-coverage-audit.json | GAP-AKO-009 | P2 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 23. Agentic Knowledge Operations / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:703 | GAP-AKO-009: Evidence Verification Agent | packages/eoip/gaps/enterprise_completion.py:14 | tests/unit/test_enterprise_gap_completion.py:7 |
| gap-coverage-audit.json | GAP-AKO-010 | P2 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 23. Agentic Knowledge Operations / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:704 | GAP-AKO-010: Query Optimization Agent | packages/eoip/gaps/enterprise_completion.py:14 | tests/unit/test_enterprise_gap_completion.py:7 |
| gap-coverage-audit.json | GAP-KFW-001 | P2 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 25. Knowledge Firewall / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:735 | GAP-KFW-001: Inspect all context leaving a knowledge boundary | packages/eoip/agents/firewall.py:4 | tests/unit/test_gap_governance_controls.py:4, tests/unit/test_gap_governance_controls.py:49, tests/unit/test_gap_governance_controls.py:174 |
| gap-coverage-audit.json | GAP-KFW-002 | P2 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 25. Knowledge Firewall / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:736 | GAP-KFW-002: Detect secrets, PII, credentials, regulated data and restricted classifications | packages/eoip/agents/firewall.py:5 | tests/unit/test_gap_governance_controls.py:5, tests/unit/test_gap_governance_controls.py:50 |
| gap-coverage-audit.json | GAP-KFW-003 | P2 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 25. Knowledge Firewall / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:737 | GAP-KFW-003: Block or redact based on policy | packages/eoip/agents/firewall.py:6 | tests/unit/test_gap_governance_controls.py:6, tests/unit/test_gap_governance_controls.py:51 |
| gap-coverage-audit.json | GAP-KFW-004 | P2 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 25. Knowledge Firewall / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:738 | GAP-KFW-004: Prevent source text from becoming executable agent instructions | packages/eoip/agents/firewall.py:7 | tests/unit/test_gap_governance_controls.py:7, tests/unit/test_gap_governance_controls.py:52 |
| gap-coverage-audit.json | GAP-KFW-005 | P2 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 25. Knowledge Firewall / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:739 | GAP-KFW-005: Tag untrusted/externally sourced graph content | packages/eoip/agents/firewall.py:8 | tests/unit/test_gap_governance_controls.py:8, tests/unit/test_gap_governance_controls.py:53 |
| gap-coverage-audit.json | GAP-KFW-006 | P2 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 25. Knowledge Firewall / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:740 | GAP-KFW-006: Defend against graph poisoning and semantic prompt injection | packages/eoip/agents/firewall.py:9 | tests/unit/test_gap_governance_controls.py:9, tests/unit/test_gap_governance_controls.py:54 |
| gap-coverage-audit.json | GAP-KFW-007 | P2 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 25. Knowledge Firewall / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:741 | GAP-KFW-007: Maintain security provenance | packages/eoip/agents/firewall.py:10 | tests/unit/test_gap_governance_controls.py:10, tests/unit/test_gap_governance_controls.py:55 |
| gap-coverage-audit.json | GAP-KFW-008 | P2 | done | 9. Phase 6 — Governed Agentic Knowledge Operations | 25. Knowledge Firewall / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:742 | GAP-KFW-008: Provide “why blocked/redacted?” explanation | packages/eoip/agents/firewall.py:11 | tests/unit/test_gap_governance_controls.py:11, tests/unit/test_gap_governance_controls.py:56 |
| g2-coverage-audit.json | G2-GRAPH-BIZ-001 | P2 | done | None | 9.8 Business Intent / Capability Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:984 | G2-GRAPH-BIZ-001 | packages/eoip/gaps/g2_readiness.py:16, packages/eoip/gaps/g2_readiness.py:189, packages/eoip/graph/business_intent.py:1 | tests/unit/test_g2_readiness.py:13 |
| g2-coverage-audit.json | G2-GRAPH-BIZ-002 | P2 | done | None | 9.8 Business Intent / Capability Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:994 | G2-GRAPH-BIZ-002 | packages/eoip/gaps/g2_readiness.py:16, packages/eoip/gaps/g2_readiness.py:189, packages/eoip/graph/business_intent.py:1 | tests/unit/test_g2_readiness.py:13 |
| g2-coverage-audit.json | G2-GRAPH-BIZ-003 | P2 | done | None | 9.8 Business Intent / Capability Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:997 | G2-GRAPH-BIZ-003 | packages/eoip/gaps/g2_readiness.py:16, packages/eoip/gaps/g2_readiness.py:189, packages/eoip/graph/business_intent.py:1 | tests/unit/test_g2_readiness.py:13 |
| g2-coverage-audit.json | G2-GRAPH-DEC-001 | P2 | done | None | 9.6 Decision Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:949 | G2-GRAPH-DEC-001 | packages/eoip/gaps/g2_readiness.py:17, packages/eoip/gaps/g2_readiness.py:187, packages/eoip/graph/decisions.py:1 | tests/unit/test_g2_readiness.py:14 |
| g2-coverage-audit.json | G2-GRAPH-DEC-002 | P2 | done | None | 9.6 Decision Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:961 | G2-GRAPH-DEC-002 | packages/eoip/gaps/g2_readiness.py:17, packages/eoip/gaps/g2_readiness.py:187, packages/eoip/graph/decisions.py:1 | tests/unit/test_g2_readiness.py:14 |
| g2-coverage-audit.json | G2-GRAPH-DEC-003 | P2 | done | None | 9.6 Decision Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:964 | G2-GRAPH-DEC-003 | packages/eoip/gaps/g2_readiness.py:17, packages/eoip/gaps/g2_readiness.py:187, packages/eoip/graph/decisions.py:1 | tests/unit/test_g2_readiness.py:14 |
| g2-coverage-audit.json | G2-GRAPH-PROC-001 | P2 | done | None | 9.7 Process Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:971 | G2-GRAPH-PROC-001 | packages/eoip/gaps/g2_readiness.py:19, packages/eoip/gaps/g2_readiness.py:188 | tests/unit/test_g2_readiness.py:16 |
| g2-coverage-audit.json | G2-GRAPH-PROC-002 | P2 | done | None | 9.7 Process Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:974 | G2-GRAPH-PROC-002 | packages/eoip/gaps/g2_readiness.py:19, packages/eoip/gaps/g2_readiness.py:188 | tests/unit/test_g2_readiness.py:16 |
| g2-coverage-audit.json | G2-GRAPH-PROC-003 | P2 | done | None | 9.7 Process Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:977 | G2-GRAPH-PROC-003 | packages/eoip/gaps/g2_readiness.py:19, packages/eoip/gaps/g2_readiness.py:188 | tests/unit/test_g2_readiness.py:16 |
| g2-coverage-audit.json | G2-GRAPH-TEST-001 | P2 | done | None | 9.5 Test Intelligence Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:935 | G2-GRAPH-TEST-001 | packages/eoip/gaps/g2_readiness.py:22, packages/eoip/gaps/g2_readiness.py:186 | tests/unit/test_g2_readiness.py:19 |
| g2-coverage-audit.json | G2-GRAPH-TEST-002 | P2 | done | None | 9.5 Test Intelligence Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:939 | G2-GRAPH-TEST-002 | packages/eoip/gaps/g2_readiness.py:22, packages/eoip/gaps/g2_readiness.py:186 | tests/unit/test_g2_readiness.py:19 |
| g2-coverage-audit.json | G2-GRAPH-TEST-003 | P2 | done | None | 9.5 Test Intelligence Graph | EOIP-engg-doc-pkg/gaps2-requirements.md:942 | G2-GRAPH-TEST-003 | packages/eoip/gaps/g2_readiness.py:22, packages/eoip/gaps/g2_readiness.py:186 | tests/unit/test_g2_readiness.py:19 |
| g2-coverage-audit.json | G2-OBS-003 | P1 | done | None | 30. Observability Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:1714 | G2-OBS-003 | packages/eoip/gaps/g2_observability.py:3, packages/eoip/gaps/g2_observability.py:36, packages/eoip/gaps/g2_observability.py:37 | tests/unit/test_g2_readiness.py:24, tests/unit/test_gap_coverage.py:9, tests/unit/test_gap_coverage.py:169 |
| g2-coverage-audit.json | G2-OBS-004 | P1 | done | None | 30. Observability Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:1720 | G2-OBS-004 | packages/eoip/gaps/g2_observability.py:3, packages/eoip/gaps/g2_observability.py:41, packages/eoip/gaps/g2_observability.py:59 | tests/unit/test_g2_readiness.py:24, tests/unit/test_gap_coverage.py:9, tests/unit/test_gap_coverage.py:170 |
| g2-coverage-audit.json | G2-OBS-005 | P1 | done | None | 30. Observability Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:1723 | G2-OBS-005 | packages/eoip/gaps/g2_observability.py:3, packages/eoip/gaps/g2_observability.py:42, packages/eoip/gaps/g2_observability.py:59 | tests/unit/test_g2_readiness.py:24, tests/unit/test_gap_coverage.py:9, tests/unit/test_gap_coverage.py:171 |
| g2-coverage-audit.json | G2-OBS-006 | P1 | done | None | 30. Observability Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:1726 | G2-OBS-006 | packages/eoip/gaps/g2_observability.py:3, packages/eoip/gaps/g2_observability.py:43, packages/eoip/gaps/g2_observability.py:59 | tests/unit/test_g2_readiness.py:24, tests/unit/test_gap_coverage.py:9, tests/unit/test_gap_coverage.py:140 |
| g2-coverage-audit.json | G2-PERF-001 | P2 | done | None | 31. Performance & Scale Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:1735 | G2-PERF-001 | packages/eoip/gaps/g2_readiness.py:29, packages/eoip/gaps/g2_readiness.py:261 | tests/unit/test_g2_readiness.py:26 |
| g2-coverage-audit.json | G2-PERF-002 | P2 | done | None | 31. Performance & Scale Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:1738 | G2-PERF-002 | packages/eoip/gaps/g2_readiness.py:29, packages/eoip/gaps/g2_readiness.py:261 | tests/unit/test_g2_readiness.py:26 |
| g2-coverage-audit.json | G2-PERF-003 | P2 | done | None | 31. Performance & Scale Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:1741 | G2-PERF-003 | packages/eoip/gaps/g2_readiness.py:29, packages/eoip/gaps/g2_readiness.py:261 | tests/unit/test_g2_readiness.py:26 |
| g2-coverage-audit.json | G2-PERF-004 | P2 | done | None | 31. Performance & Scale Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:1744 | G2-PERF-004 | packages/eoip/gaps/g2_readiness.py:29, packages/eoip/gaps/g2_readiness.py:261 | tests/unit/test_g2_readiness.py:26 |
| g2-coverage-audit.json | G2-PERF-005 | P2 | done | None | 31. Performance & Scale Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:1747 | G2-PERF-005 | packages/eoip/gaps/g2_readiness.py:29, packages/eoip/gaps/g2_readiness.py:261 | tests/unit/test_g2_readiness.py:26 |
| g2-coverage-audit.json | G2-PERF-006 | P2 | done | None | 31. Performance & Scale Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:1750 | G2-PERF-006 | packages/eoip/gaps/g2_readiness.py:29, packages/eoip/gaps/g2_readiness.py:261 | tests/unit/test_g2_readiness.py:26 |
| g2-coverage-audit.json | G2-PERF-007 | P2 | done | None | 31. Performance & Scale Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:1753 | G2-PERF-007 | packages/eoip/gaps/g2_readiness.py:29, packages/eoip/gaps/g2_readiness.py:261 | tests/unit/test_g2_readiness.py:26 |
| g2-coverage-audit.json | G2-PERF-008 | P2 | done | None | 31. Performance & Scale Requirements | EOIP-engg-doc-pkg/gaps2-requirements.md:1756 | G2-PERF-008 | packages/eoip/gaps/g2_readiness.py:29, packages/eoip/gaps/g2_readiness.py:261 | tests/unit/test_g2_readiness.py:26 |
| gap-coverage-audit.json | GAP-AI-001 | P0 | done | None | 4. Competitive Study / 4.2 Neo4j / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:147 | GAP-AI-001: Make every GraphRAG/agent answer evidence-addressable to graph nodes, paths and source records | packages/eoip/provenance/evidence.py:12 | tests/unit/test_gap_governance_controls.py:25, tests/unit/test_gap_governance_controls.py:114 |
| gap-coverage-audit.json | GAP-CDC-001 | P1 | done | None | 29. Graph Change Data Capture / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:803 | GAP-CDC-001: Every graph mutation emits an internal event | packages/eoip/future_scope.py:65, packages/eoip/future_scope.py:638, packages/eoip/gaps/enterprise_completion.py:18 | tests/unit/test_enterprise_gap_completion.py:11 |
| gap-coverage-audit.json | GAP-CDC-002 | P1 | done | None | 29. Graph Change Data Capture / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:804 | GAP-CDC-002: Event includes before/after semantic identity | packages/eoip/gaps/enterprise_completion.py:18 | tests/unit/test_enterprise_gap_completion.py:11 |
| gap-coverage-audit.json | GAP-CDC-003 | P1 | done | None | 29. Graph Change Data Capture / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:805 | GAP-CDC-003: Consumers can subscribe to entity/edge/domain changes | packages/eoip/future_scope.py:66, packages/eoip/future_scope.py:654, packages/eoip/gaps/enterprise_completion.py:18 | tests/unit/test_enterprise_gap_completion.py:11 |
| gap-coverage-audit.json | GAP-CDC-004 | P1 | done | None | 29. Graph Change Data Capture / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:806 | GAP-CDC-004: Support incremental search/vector/index synchronization | packages/eoip/future_scope.py:67, packages/eoip/future_scope.py:654, packages/eoip/gaps/enterprise_completion.py:18 | tests/unit/test_enterprise_gap_completion.py:11 |
| gap-coverage-audit.json | GAP-CDC-005 | P1 | done | None | 29. Graph Change Data Capture / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:807 | GAP-CDC-005: Support incremental GraphRAG summary update | packages/eoip/future_scope.py:68, packages/eoip/future_scope.py:654, packages/eoip/gaps/enterprise_completion.py:18 | tests/unit/test_enterprise_gap_completion.py:11 |
| gap-coverage-audit.json | GAP-CDC-006 | P1 | done | None | 29. Graph Change Data Capture / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:808 | GAP-CDC-006: Replay from checkpoint | packages/eoip/future_scope.py:69, packages/eoip/future_scope.py:638, packages/eoip/future_scope.py:654 | tests/unit/test_enterprise_gap_completion.py:11 |
| gap-coverage-audit.json | GAP-DRIFT-001 | P1 | done | None | 13. Semantic Drift Detection / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:513 | GAP-DRIFT-001: Detect source schema drift | packages/eoip/gaps/enterprise_completion.py:24 | tests/unit/test_enterprise_gap_completion.py:17 |
| gap-coverage-audit.json | GAP-DRIFT-002 | P1 | done | None | 13. Semantic Drift Detection / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:514 | GAP-DRIFT-002: Detect ontology drift | packages/eoip/gaps/enterprise_completion.py:24 | tests/unit/test_enterprise_gap_completion.py:17 |
| gap-coverage-audit.json | GAP-DRIFT-003 | P1 | done | None | 13. Semantic Drift Detection / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:515 | GAP-DRIFT-003: Detect vocabulary usage drift | packages/eoip/gaps/enterprise_completion.py:24 | tests/unit/test_enterprise_gap_completion.py:17 |
| gap-coverage-audit.json | GAP-DRIFT-004 | P1 | done | None | 13. Semantic Drift Detection / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:516 | GAP-DRIFT-004: Detect relationship distribution shifts | packages/eoip/gaps/enterprise_completion.py:24 | tests/unit/test_enterprise_gap_completion.py:17 |
| gap-coverage-audit.json | GAP-DRIFT-005 | P1 | done | None | 13. Semantic Drift Detection / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:517 | GAP-DRIFT-005: Detect embedding-space drift if vector retrieval is used | packages/eoip/gaps/enterprise_completion.py:24, packages/eoip/ontology/embedding_drift.py:1 | tests/unit/test_enterprise_gap_completion.py:17 |
| gap-coverage-audit.json | GAP-DRIFT-006 | P1 | done | None | 13. Semantic Drift Detection / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:518 | GAP-DRIFT-006: Detect code architecture drift from intended ontology/architecture | packages/eoip/gaps/enterprise_completion.py:24 | tests/unit/test_enterprise_gap_completion.py:17 |
| gap-coverage-audit.json | GAP-DRIFT-007 | P1 | done | None | 13. Semantic Drift Detection / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:519 | GAP-DRIFT-007: Generate drift explanations and affected assets | packages/eoip/gaps/enterprise_completion.py:25 | tests/unit/test_enterprise_gap_completion.py:18 |
| gap-coverage-audit.json | GAP-DUAL-001 | P2 | done | None | 4. Competitive Study / 4.2 Neo4j / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:142 | GAP-DUAL-001: Implement a Dual Semantic Model: native HugeGraph property graph + canonical RDF/OWL/SHACL semantic representation | packages/eoip/future_scope.py:11, packages/eoip/future_scope.py:40, packages/eoip/future_scope.py:152 | tests/unit/test_enterprise_gap_completion.py:19 |
| gap-coverage-audit.json | GAP-DUAL-002 | P2 | done | None | 4. Competitive Study / 4.2 Neo4j / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:143 | GAP-DUAL-002: Guarantee round-trip mappings for supported ontology constructs | packages/eoip/future_scope.py:11, packages/eoip/future_scope.py:41, packages/eoip/future_scope.py:179 | tests/unit/test_enterprise_gap_completion.py:19 |
| gap-coverage-audit.json | GAP-ENG-001 | P2 | done | None | 4. Competitive Study / 4.1 Stardog / Requirements to turn these trade-offs into strengths | EOIP-engg-doc-pkg/gaps-requirements.md:121 | GAP-ENG-001: Make requirement-to-code-to-runtime traceability a native differentiator rather than an external integration | packages/eoip/gaps/enterprise_completion.py:26 | tests/unit/test_enterprise_gap_completion.py:19 |
| gap-coverage-audit.json | GAP-ER-001 | P1 | done | None | 19. Enterprise Entity Resolution Workbench / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:621 | GAP-ER-001: Deterministic match rules | packages/eoip/gaps/enterprise_completion.py:27, packages/eoip/identity/candidates.py:1 | tests/unit/test_enterprise_gap_completion.py:20 |
| gap-coverage-audit.json | GAP-ER-002 | P1 | done | None | 19. Enterprise Entity Resolution Workbench / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:622 | GAP-ER-002: Probabilistic/fuzzy match | packages/eoip/gaps/enterprise_completion.py:27, packages/eoip/identity/candidates.py:1 | tests/unit/test_enterprise_gap_completion.py:20 |
| gap-coverage-audit.json | GAP-ER-003 | P1 | done | None | 19. Enterprise Entity Resolution Workbench / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:623 | GAP-ER-003: Configurable match features | packages/eoip/gaps/enterprise_completion.py:27, packages/eoip/identity/candidates.py:1 | tests/unit/test_enterprise_gap_completion.py:20 |
| gap-coverage-audit.json | GAP-ER-004 | P1 | done | None | 19. Enterprise Entity Resolution Workbench / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:624 | GAP-ER-004: Explain match score | packages/eoip/gaps/enterprise_completion.py:27, packages/eoip/identity/candidates.py:1 | tests/unit/test_enterprise_gap_completion.py:20 |
| gap-coverage-audit.json | GAP-ER-005 | P1 | done | None | 19. Enterprise Entity Resolution Workbench / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:625 | GAP-ER-005: Candidate queue for human review | packages/eoip/identity/candidates.py:1, apps/api/main.py:1236 | tests/unit/test_identity_candidates.py:1 |
| gap-coverage-audit.json | GAP-ER-006 | P1 | done | None | 19. Enterprise Entity Resolution Workbench / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:626 | GAP-ER-006: Merge/unmerge | packages/eoip/gaps/enterprise_completion.py:27, packages/eoip/identity/candidates.py:1 | tests/unit/test_enterprise_gap_completion.py:20 |
| gap-coverage-audit.json | GAP-ER-007 | P1 | done | None | 19. Enterprise Entity Resolution Workbench / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:627 | GAP-ER-007: Golden entity record | packages/eoip/gaps/enterprise_completion.py:27, packages/eoip/identity/candidates.py:1 | tests/unit/test_enterprise_gap_completion.py:20 |
| gap-coverage-audit.json | GAP-ER-008 | P1 | done | None | 19. Enterprise Entity Resolution Workbench / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:628 | GAP-ER-008: Source aliases | packages/eoip/gaps/enterprise_completion.py:27, packages/eoip/identity/candidates.py:1 | tests/unit/test_enterprise_gap_completion.py:20 |
| gap-coverage-audit.json | GAP-ER-009 | P1 | done | None | 19. Enterprise Entity Resolution Workbench / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:629 | GAP-ER-009: Historical identity evolution | packages/eoip/gaps/enterprise_completion.py:28, packages/eoip/identity/candidates.py:1 | tests/unit/test_enterprise_gap_completion.py:21 |
| gap-coverage-audit.json | GAP-ER-010 | P1 | done | None | 19. Enterprise Entity Resolution Workbench / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:630 | GAP-ER-010: No irreversible automatic merge below confidence threshold | packages/eoip/gaps/enterprise_completion.py:28, packages/eoip/identity/candidates.py:1 | tests/unit/test_enterprise_gap_completion.py:21 |
| gap-coverage-audit.json | GAP-EXPORT-001 | P2 | done | None | 4. Competitive Study / 4.10 Oracle RDF Graph / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:339 | GAP-EXPORT-001: Support RDF, JSON-LD, GraphML/CSV and canonical JSON exports | packages/eoip/gaps/enterprise_completion.py:29 | tests/unit/test_enterprise_gap_completion.py:22 |
| gap-coverage-audit.json | GAP-HG-006 | P0 | done | None | 44. HugeGraph-Specific Hardening / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:1079 | GAP-HG-006: standalone → distributed migration playbook | packages/eoip/gaps/enterprise_completion.py:32, deploy/docker-compose.ha.yml:128 | tests/unit/test_enterprise_gap_completion.py:25 |
| gap-coverage-audit.json | GAP-HG-007 | P0 | done | None | 44. HugeGraph-Specific Hardening / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:1080 | GAP-HG-007: backup/restore verification | packages/eoip/gaps/enterprise_completion.py:32 | tests/unit/test_enterprise_gap_completion.py:25 |
| gap-coverage-audit.json | GAP-HG-008 | P0 | done | None | 44. HugeGraph-Specific Hardening / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:1081 | GAP-HG-008: capacity benchmark before production | packages/eoip/gaps/enterprise_completion.py:33, packages/eoip/graph/benchmark.py:1 | tests/unit/test_enterprise_gap_completion.py:26 |
| gap-coverage-audit.json | GAP-HG-009 | P0 | done | None | 44. HugeGraph-Specific Hardening / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:1082 | GAP-HG-009: Gremlin query safety | packages/eoip/gaps/enterprise_completion.py:33 | tests/unit/test_enterprise_gap_completion.py:26 |
| gap-coverage-audit.json | GAP-HG-010 | P0 | done | None | 44. HugeGraph-Specific Hardening / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:1083 | GAP-HG-010: avoid pretending SPARQL/RDF is native; use explicit semantic adapter | packages/eoip/gaps/enterprise_completion.py:33 | tests/unit/test_enterprise_gap_completion.py:26 |
| gap-coverage-audit.json | GAP-IDE-001 | P2 | done | None | 4. Competitive Study / 4.3 Ontotext GraphDB / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:173 | GAP-IDE-001: Expose ontology and lineage directly within VS Code | packages/eoip/gaps/enterprise_completion.py:34 | tests/unit/test_enterprise_gap_completion.py:27 |
| gap-coverage-audit.json | GAP-KGCI-001 | P0 | done | None | 30. Knowledge Graph CI/CD / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:820 | GAP-KGCI-001: CLI runnable in CI | packages/eoip/ci/pipeline.py:1, packages/eoip/ci/pipeline.py:5, packages/eoip/ci/pipeline.py:6 | tests/unit/test_gap_coverage.py:5, tests/unit/test_gap_coverage.py:44, tests/unit/test_gap_coverage.py:187 |
| gap-coverage-audit.json | GAP-KGCI-002 | P0 | done | None | 30. Knowledge Graph CI/CD / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:821 | GAP-KGCI-002: Machine-readable report | packages/eoip/ci/pipeline.py:1, packages/eoip/ci/pipeline.py:112, packages/eoip/ci/pipeline.py:166 | tests/unit/test_gap_coverage.py:6, tests/unit/test_gap_coverage.py:37, tests/unit/test_gap_coverage.py:54 |
| gap-coverage-audit.json | GAP-KGCI-003 | P0 | done | None | 30. Knowledge Graph CI/CD / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:822 | GAP-KGCI-003: Fail build on configured semantic regression | packages/eoip/ci/pipeline.py:1, packages/eoip/ci/pipeline.py:74, packages/eoip/ci/pipeline.py:166 | tests/unit/test_gap_coverage.py:7, tests/unit/test_gap_coverage.py:90, tests/unit/test_gap_coverage.py:187 |
| gap-coverage-audit.json | GAP-KGCI-004 | P0 | done | None | 30. Knowledge Graph CI/CD / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:823 | GAP-KGCI-004: Generate versioned ontology artifact | packages/eoip/ci/pipeline.py:1, packages/eoip/ci/pipeline.py:126, packages/eoip/ci/pipeline.py:166 | tests/unit/test_kgci_pipeline.py:1, tests/unit/test_kgci_pipeline.py:91 |
| gap-coverage-audit.json | GAP-LIFE-001 | P2 | done | None | 35. Knowledge Compaction & Lifecycle / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:900 | GAP-LIFE-001: Tier hot/warm/archive graph information | packages/eoip/future_scope.py:77, packages/eoip/future_scope.py:740, packages/eoip/gaps/enterprise_completion.py:38 | tests/unit/test_enterprise_gap_completion.py:31 |
| gap-coverage-audit.json | GAP-LIFE-002 | P2 | done | None | 35. Knowledge Compaction & Lifecycle / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:901 | GAP-LIFE-002: Archive historical facts without losing lineage | packages/eoip/future_scope.py:78, packages/eoip/future_scope.py:740, packages/eoip/gaps/enterprise_completion.py:38 | tests/unit/test_enterprise_gap_completion.py:31 |
| gap-coverage-audit.json | GAP-LIFE-003 | P2 | done | None | 35. Knowledge Compaction & Lifecycle / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:902 | GAP-LIFE-003: Expire transient agent memory separately from enterprise facts | packages/eoip/future_scope.py:79, packages/eoip/future_scope.py:740, packages/eoip/gaps/enterprise_completion.py:38 | tests/unit/test_enterprise_gap_completion.py:31 |
| gap-coverage-audit.json | GAP-LIFE-004 | P2 | done | None | 35. Knowledge Compaction & Lifecycle / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:903 | GAP-LIFE-004: Retention policies per domain/classification | packages/eoip/future_scope.py:80, packages/eoip/future_scope.py:740, packages/eoip/gaps/enterprise_completion.py:38 | tests/unit/test_enterprise_gap_completion.py:31 |
| gap-coverage-audit.json | GAP-LIFE-005 | P2 | done | None | 35. Knowledge Compaction & Lifecycle / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:904 | GAP-LIFE-005: Purge with provenance record where legally allowed | packages/eoip/future_scope.py:81, packages/eoip/future_scope.py:740, packages/eoip/gaps/enterprise_completion.py:39 | tests/unit/test_enterprise_gap_completion.py:32 |
| gap-coverage-audit.json | GAP-LIFE-006 | P2 | done | None | 35. Knowledge Compaction & Lifecycle / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:905 | GAP-LIFE-006: Rebuild derived data from authoritative inputs | packages/eoip/future_scope.py:82, packages/eoip/future_scope.py:740, packages/eoip/gaps/enterprise_completion.py:39 | tests/unit/test_enterprise_gap_completion.py:32 |
| gap-coverage-audit.json | GAP-MIGRATION-001 | P2 | done | None | 4. Competitive Study / 4.10 Oracle RDF Graph / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:340 | GAP-MIGRATION-001: Provide migration utilities and stable external IDs | packages/eoip/gaps/enterprise_completion.py:41 | tests/unit/test_enterprise_gap_completion.py:34 |
| gap-coverage-audit.json | GAP-NLP-001 | P2 | done | None | 4. Competitive Study / 4.5 PoolParty Semantic Suite / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:222 | GAP-NLP-001: Add local entity extraction, tagging, classification and concept recommendation | packages/eoip/gaps/enterprise_completion.py:41 | tests/unit/test_enterprise_gap_completion.py:34 |
| gap-coverage-audit.json | GAP-NOCODE-001 | P0 | done | None | 4. Competitive Study / 4.4 TopBraid EDG / TQ Data Foundation / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:194 | GAP-NOCODE-001: Build a visual Ontology Studio for ontology classes, properties, edges, SHACL-like constraints and mappings | packages/eoip/gaps/enterprise_completion.py:42, apps/web/src/studio/Studio.jsx:13 | tests/unit/test_enterprise_gap_completion.py:35 |
| gap-coverage-audit.json | GAP-NOCODE-002 | P0 | done | None | 4. Competitive Study / 4.4 TopBraid EDG / TQ Data Foundation / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:195 | GAP-NOCODE-002: Provide novice, analyst and expert editing modes | packages/eoip/gaps/enterprise_completion.py:42, apps/web/src/studio/Studio.jsx:14 | tests/unit/test_enterprise_gap_completion.py:35 |
| gap-coverage-audit.json | GAP-NOCODE-003 | P0 | done | None | 4. Competitive Study / 4.4 TopBraid EDG / TQ Data Foundation / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:196 | GAP-NOCODE-003: Generate forms, GraphQL/OpenAPI schemas and validation rules from ontology definitions where feasible | packages/eoip/gaps/enterprise_completion.py:42, apps/web/src/studio/Studio.jsx:15 | tests/unit/test_enterprise_gap_completion.py:35 |
| gap-coverage-audit.json | GAP-PACK-001 | P2 | done | None | 4. Competitive Study / 4.5 PoolParty Semantic Suite / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:224 | GAP-PACK-001: Keep major core capabilities integrated in one platform while allowing optional modules rather than artificial fragmentation | packages/eoip/gaps/enterprise_completion.py:44 | tests/unit/test_enterprise_gap_completion.py:37 |
| gap-coverage-audit.json | GAP-PROV-007 | P0 | done | None | 10. Provenance & Evidence Ledger / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:460 | GAP-PROV-007: Evidence manifests must be exportable and immutable after issuance | packages/eoip/gaps/enterprise_completion.py:45 | tests/unit/test_enterprise_gap_completion.py:38 |
| gap-coverage-audit.json | GAP-PROV-008 | P0 | done | None | 10. Provenance & Evidence Ledger / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:461 | GAP-PROV-008: Provide “why does this edge exist?” UI | packages/eoip/gaps/enterprise_completion.py:45 | tests/unit/test_enterprise_gap_completion.py:38 |
| gap-coverage-audit.json | GAP-PROV-009 | P0 | done | None | 10. Provenance & Evidence Ledger / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:462 | GAP-PROV-009: Provide “what would disappear if source X were removed?” analysis | packages/eoip/gaps/enterprise_completion.py:45 | tests/unit/test_enterprise_gap_completion.py:38 |
| gap-coverage-audit.json | GAP-QUERY-001 | P2 | done | None | 4. Competitive Study / 4.9 Amazon Neptune / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:321 | GAP-QUERY-001: Provide one Unified Semantic Query API capable of routing internally to Gremlin, semantic/RDF adapter, search, vector or federated source | packages/eoip/gaps/enterprise_completion.py:46 | tests/unit/test_enterprise_gap_completion.py:39 |
| gap-coverage-audit.json | GAP-REC-001 | P2 | done | None | 4. Competitive Study / 4.5 PoolParty Semantic Suite / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:223 | GAP-REC-001: Add graph-aware recommendation engine for documents, experts, components and related concepts | packages/eoip/graph/expertise.py:1, apps/api/app.py:924 | tests/unit/test_expertise_freshness.py:1 |
| gap-coverage-audit.json | GAP-RULE-001 | P2 | done | None | 4. Competitive Study / 4.3 Ontotext GraphDB / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:170 | GAP-RULE-001: Build a deterministic rules engine supporting versioned inference policies | packages/eoip/future_scope.py:12, packages/eoip/future_scope.py:42, packages/eoip/future_scope.py:195 | tests/unit/test_enterprise_gap_completion.py:41 |
| gap-coverage-audit.json | GAP-RULE-002 | P2 | done | None | 4. Competitive Study / 4.3 Ontotext GraphDB / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:171 | GAP-RULE-002: Distinguish asserted, inferred, model-generated and human-confirmed facts | packages/eoip/provenance/trust.py:9 | tests/unit/test_gap_governance_controls.py:19, tests/unit/test_gap_governance_controls.py:82 |
| gap-coverage-audit.json | GAP-RULE-003 | P2 | done | None | 4. Competitive Study / 4.3 Ontotext GraphDB / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:172 | GAP-RULE-003: Support retraction/recomputation when source assertions change | packages/eoip/future_scope.py:12, packages/eoip/future_scope.py:43, packages/eoip/future_scope.py:239 | tests/unit/test_enterprise_gap_completion.py:41 |
| gap-coverage-audit.json | GAP-SEC-001 | P1 | done | None | 27. Fine-Grained Security Roadmap | EOIP-engg-doc-pkg/gaps-requirements.md:783 | GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | packages/eoip/authn/__init__.py:1, packages/eoip/authn/__init__.py:56, packages/eoip/authn/__init__.py:60 | tests/unit/test_authn.py:1, tests/unit/test_authz.py:1 |
| gap-coverage-audit.json | GAP-SEC-002 | P1 | done | None | 27. Fine-Grained Security Roadmap | EOIP-engg-doc-pkg/gaps-requirements.md:783 | GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | packages/eoip/authn/__init__.py:1, packages/eoip/authn/__init__.py:12, packages/eoip/authn/__init__.py:116 | tests/unit/test_authn.py:1, tests/unit/test_authz.py:1, tests/unit/test_authz.py:53 |
| gap-coverage-audit.json | GAP-SEC-003 | P1 | done | None | 27. Fine-Grained Security Roadmap | EOIP-engg-doc-pkg/gaps-requirements.md:783 | GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | packages/eoip/authn/__init__.py:1, packages/eoip/authn/__init__.py:15, packages/eoip/authn/__init__.py:116 | tests/unit/test_authn.py:1, tests/unit/test_authn.py:305, tests/unit/test_authz.py:1 |
| gap-coverage-audit.json | GAP-SEC-004 | P1 | done | None | 27. Fine-Grained Security Roadmap | EOIP-engg-doc-pkg/gaps-requirements.md:783 | GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | packages/eoip/authn/__init__.py:1, packages/eoip/authn/__init__.py:68, packages/eoip/authn/__init__.py:254 | tests/unit/test_authn.py:1, tests/unit/test_authz.py:1, tests/unit/test_authz.py:90 |
| gap-coverage-audit.json | GAP-SEC-005 | P1 | done | None | 27. Fine-Grained Security Roadmap | EOIP-engg-doc-pkg/gaps-requirements.md:783 | GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | packages/eoip/authz/core.py:1, packages/eoip/authz/core.py:15, packages/eoip/authz/core.py:283 | tests/unit/test_authz.py:1, tests/unit/test_authz.py:226 |
| gap-coverage-audit.json | GAP-SEC-006 | P1 | done | None | 27. Fine-Grained Security Roadmap | EOIP-engg-doc-pkg/gaps-requirements.md:783 | GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | packages/eoip/authz/core.py:1, packages/eoip/authz/core.py:15, packages/eoip/authz/core.py:283 | tests/unit/test_authz.py:1, tests/unit/test_authz.py:226 |
| gap-coverage-audit.json | GAP-SEC-007 | P1 | done | None | 27. Fine-Grained Security Roadmap | EOIP-engg-doc-pkg/gaps-requirements.md:783 | GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | packages/eoip/authz/tokens.py:1, packages/eoip/authz/tokens.py:38, packages/eoip/authz/__init__.py:1 | tests/unit/test_authz.py:1, tests/unit/test_authz.py:260 |
| gap-coverage-audit.json | GAP-SEC-008 | P1 | done | None | 27. Fine-Grained Security Roadmap | EOIP-engg-doc-pkg/gaps-requirements.md:783 | GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | packages/eoip/authz/tokens.py:1, packages/eoip/authz/tokens.py:6, packages/eoip/authz/tokens.py:20 | tests/unit/test_authz.py:1, tests/unit/test_authz.py:260 |
| gap-coverage-audit.json | GAP-SEC-009 | P1 | done | None | 27. Fine-Grained Security Roadmap | EOIP-engg-doc-pkg/gaps-requirements.md:783 | GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | packages/eoip/authz/tokens.py:1, packages/eoip/authz/tokens.py:33, packages/eoip/authz/__init__.py:1 | tests/unit/test_authz.py:1, tests/unit/test_authz.py:260 |
| gap-coverage-audit.json | GAP-SEC-010 | P1 | done | None | 27. Fine-Grained Security Roadmap | EOIP-engg-doc-pkg/gaps-requirements.md:783 | GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | packages/eoip/authz/__init__.py:1 | tests/unit/test_authz.py:1 |
| gap-coverage-audit.json | GAP-SEC-011 | P1 | done | None | 27. Fine-Grained Security Roadmap | EOIP-engg-doc-pkg/gaps-requirements.md:783 | GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | packages/eoip/authz/__init__.py:1 | tests/unit/test_authz.py:1 |
| gap-coverage-audit.json | GAP-SEC-012 | P1 | done | None | 27. Fine-Grained Security Roadmap | EOIP-engg-doc-pkg/gaps-requirements.md:783 | GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | packages/eoip/authz/__init__.py:1 | tests/unit/test_authz.py:1, tests/unit/test_gap_coverage.py:45 |
| gap-coverage-audit.json | GAP-SEM-001 | P2 | done | None | 4. Competitive Study / 4.2 Neo4j / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:146 | GAP-SEM-001: Treat ontology/schema/governance as first-class, not a plugin | packages/eoip/gaps/enterprise_completion.py:51 | tests/unit/test_enterprise_gap_completion.py:44 |
| gap-coverage-audit.json | GAP-TCO-001 | P2 | done | None | 4. Competitive Study / 4.5 PoolParty Semantic Suite / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:225 | GAP-TCO-001: Provide transparent resource consumption, sizing calculator and offline license/deployment model | packages/eoip/future_scope.py:17, packages/eoip/future_scope.py:50, packages/eoip/future_scope.py:396 | tests/unit/test_enterprise_gap_completion.py:47 |
| gap-coverage-audit.json | GAP-TEMP-001 | P1 | done | None | 16. Temporal / Bitemporal Knowledge / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:568 | GAP-TEMP-001: Support event time and system/ingestion time | packages/eoip/graph/bitemporal.py:1, packages/eoip/graph/bitemporal.py:72, packages/eoip/graph/bitemporal.py:206 | tests/unit/test_bitemporal.py:116 |
| gap-coverage-audit.json | GAP-TEMP-002 | P1 | done | None | 16. Temporal / Bitemporal Knowledge / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:569 | GAP-TEMP-002: Query “what was known at time T?” | packages/eoip/graph/bitemporal.py:1, packages/eoip/graph/bitemporal.py:72, packages/eoip/graph/bitemporal.py:218 | tests/unit/test_bitemporal.py:135 |
| gap-coverage-audit.json | GAP-TEMP-003 | P1 | done | None | 16. Temporal / Bitemporal Knowledge / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:570 | GAP-TEMP-003: Query “what was actually valid at time T?” | packages/eoip/graph/bitemporal.py:1, packages/eoip/graph/bitemporal.py:43, packages/eoip/graph/bitemporal.py:72 | tests/unit/test_bitemporal.py:150 |
| gap-coverage-audit.json | GAP-TEMP-004 | P1 | done | None | 16. Temporal / Bitemporal Knowledge / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:571 | GAP-TEMP-004: Support historical topology reconstruction | packages/eoip/graph/bitemporal.py:1, packages/eoip/graph/bitemporal.py:92, packages/eoip/graph/bitemporal.py:244 | tests/unit/test_bitemporal.py:169 |
| gap-coverage-audit.json | GAP-TEMP-005 | P1 | done | None | 16. Temporal / Bitemporal Knowledge / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:572 | GAP-TEMP-005: Retain semantic changes without overwriting history | packages/eoip/graph/bitemporal.py:1, packages/eoip/graph/bitemporal.py:112, packages/eoip/graph/bitemporal.py:272 | tests/unit/test_bitemporal.py:193 |
| gap-coverage-audit.json | GAP-TEMP-006 | P1 | done | None | 16. Temporal / Bitemporal Knowledge / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:573 | GAP-TEMP-006: Graph diffs must be first-class objects | packages/eoip/gaps/enterprise_completion.py:54 | tests/unit/test_enterprise_gap_completion.py:47 |
| gap-coverage-audit.json | GAP-UX-001 | P2 | done | None | 4. Competitive Study / 4.4 TopBraid EDG / TQ Data Foundation / Requirements | EOIP-engg-doc-pkg/gaps-requirements.md:200 | GAP-UX-001: Hide RDF/SHACL complexity from non-semantic users while preserving standards internally | packages/eoip/gaps/enterprise_completion.py:54 | tests/unit/test_enterprise_gap_completion.py:47 |

## Per-Document Line Coverage Digest

This digest is the line-level accounting layer. For each Markdown file, all lines were read; the table records line count, first and last line text, and every heading with its source line. This prevents silent omission of short files, demo files, tickets, diagrams, and runbooks.

### agent_runbook.md

| Property | Value |
| --- | --- |
| Lines read | 83 |
| Nonblank lines | 72 |
| SHA-256 prefix | 0e916fd7a4cf5e61 |
| First line | # EOIP Agent Runbook |
| Last line | never hidden by an unconditional subsequent success. |
| Requirement-like lines | 22 |
| Status/gap/risk-like lines | 4 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Agent Runbook |
| 6 | ## Start, work and stop |
| 18 | ## Verified repository command catalog |
| 74 | ## Naming and publication |

### apps/vscode-extension/README.md

| Property | Value |
| --- | --- |
| Lines read | 83 |
| Nonblank lines | 70 |
| SHA-256 prefix | 3cf71126124c906a |
| First line | # EOIP Context |
| Last line | visible VS Code development host; it does not install or certify a VSIX. |
| Requirement-like lines | 20 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Context |

### checklist.md

| Property | Value |
| --- | --- |
| Lines read | 112 |
| Nonblank lines | 97 |
| SHA-256 prefix | 25391d02c12abc2e |
| First line | # EOIP Coordination and Completion Checklist |
| Last line | triage and not independent product acceptance. |
| Requirement-like lines | 34 |
| Status/gap/risk-like lines | 15 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Coordination and Completion Checklist |
| 6 | ## Ticket rollup |
| 16 | ## Guided enterprise demo (ticket-20261004-005) |
| 39 | ## Coordination gate (ticket-20261004-002) |
| 55 | ## Audit evidence foundation (ticket-20261004-004) |
| 75 | ## Product acceptance gates (ticket-20261004-003) |

### context.md

| Property | Value |
| --- | --- |
| Lines read | 98 |
| Nonblank lines | 82 |
| SHA-256 prefix | 879fa7625e9dc9a4 |
| First line | **Persona**: You are the Senior Engineer. Resolve EOIP's cross-component defects at their root while preserving tested contracts and behavior. |
| Last line | [handoff template](handoff_template.md). |
| Requirement-like lines | 27 |
| Status/gap/risk-like lines | 6 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 3 | # EOIP Current Coordination Context |
| 20 | ## Goal and scope |
| 36 | ## Actual components |
| 54 | ## Commands and evidence |
| 84 | ## Working tree and next work |

### demo/autodemo/README.md

| Property | Value |
| --- | --- |
| Lines read | 158 |
| Nonblank lines | 138 |
| SHA-256 prefix | 1d668daf381358c7 |
| First line | # EOIP client demonstrations |
| Last line | than inferring complete coverage from a successful console exit. |
| Requirement-like lines | 46 |
| Status/gap/risk-like lines | 7 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP client demonstrations |
| 18 | ## Prerequisites and safe operation |
| 43 | ## Visible sequences and coverage boundaries |
| 113 | ## Running and pacing |
| 145 | ## Validation strategy |

### demo/autodemo/runtime-validation-report.md

| Property | Value |
| --- | --- |
| Lines read | 68 |
| Nonblank lines | 57 |
| SHA-256 prefix | 9adc5a0f7b3dc0e7 |
| First line | # VS Code Auto-Demo Validation |
| Last line | Reproduce with the commands above and prerequisites in [README](README.md). |
| Requirement-like lines | 16 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # VS Code Auto-Demo Validation |
| 23 | ## Live scope |
| 45 | ## Environment and boundaries |

### demo/demodata/code/README.md

| Property | Value |
| --- | --- |
| Lines read | 52 |
| Nonblank lines | 41 |
| SHA-256 prefix | 7e943d98fcee1ac8 |
| First line | # Code Graph Demo Data — Meridian Financial Services |
| Last line | ``` |
| Requirement-like lines | 5 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Code Graph Demo Data — Meridian Financial Services |
| 13 | ## Source Repositories |
| 22 | ## Key Infrastructure References |
| 30 | ## Cross-Repository Connections |
| 38 | ## JSON Format |

### demo/demodata/core/demo-repo/README.md

| Property | Value |
| --- | --- |
| Lines read | 4 |
| Nonblank lines | 3 |
| SHA-256 prefix | b23a7c8fb1478172 |
| First line | # EOIP-1 requirement trace |
| Last line | the Python math module. EOIP-2 requires the path to retain source evidence. |
| Requirement-like lines | 1 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen | EOIP-1, EOIP-2 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP-1 requirement trace |

### demo/demodata/crawler/README.md

| Property | Value |
| --- | --- |
| Lines read | 48 |
| Nonblank lines | 38 |
| SHA-256 prefix | b91e6d798dca0744 |
| First line | # Crawler Demo Data — Meridian Financial Services |
| Last line | ``` |
| Requirement-like lines | 10 |
| Status/gap/risk-like lines | 1 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Crawler Demo Data — Meridian Financial Services |
| 12 | ## Source Portals |
| 22 | ## Key Cross-References |
| 34 | ## JSON Format |

### demo/demodata/enterprise/README.md

| Property | Value |
| --- | --- |
| Lines read | 63 |
| Nonblank lines | 49 |
| SHA-256 prefix | 11ee286a9add3da0 |
| First line | # Northstar enterprise demo pack |
| Last line | Every scenario reports `ready: true` only when each expected graph entity is actually present. |
| Requirement-like lines | 16 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Northstar enterprise demo pack |
| 5 | ## What is included |
| 25 | ## Guided Hubble demonstration |
| 50 | ## Quick verification |

### demo/demodata/enterprise/wiki/checkout-latency-runbook.md

| Property | Value |
| --- | --- |
| Lines read | 12 |
| Nonblank lines | 9 |
| SHA-256 prefix | bd18c1105504516c |
| First line | # Checkout latency incident runbook |
| Last line | Rollback authority belongs to Commerce SRE. Emergency changes require an auditable ServiceNow approval. |
| Requirement-like lines | 3 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Checkout latency incident runbook |

### demo/demodata/enterprise/wiki/checkout-risk-architecture.md

| Property | Value |
| --- | --- |
| Lines read | 34 |
| Nonblank lines | 23 |
| SHA-256 prefix | d95bc157842bc188 |
| First line | # Checkout risk architecture |
| Last line | TC-884 proves the low-risk contract and TC-901 proves timeout behavior. Pipeline 4815 must complete contract tests before the production deployment job can run. |
| Requirement-like lines | 5 |
| Status/gap/risk-like lines | 5 |
| Requirement IDs seen | ADR-COM-014 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Checkout risk architecture |
| 8 | ## Context |
| 12 | ## Runtime flow |
| 20 | ## Reliability boundary |
| 24 | ## Failure modes and safe fallback |
| 32 | ## Verification |

### demo/demodata/manual/README.md

| Property | Value |
| --- | --- |
| Lines read | 56 |
| Nonblank lines | 45 |
| SHA-256 prefix | b3829afdbcf01b5d |
| First line | # Manual Demo Data - Meridian Financial Services (MFS) |
| Last line | use completely different work item keys and project domains. |
| Requirement-like lines | 8 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Manual Demo Data - Meridian Financial Services (MFS) |
| 3 | ## Scenario: Payment Gateway Modernization (PAY Project) |
| 16 | ## Data Sources |
| 34 | ## Infrastructure |
| 41 | ## Cross-Reference Integrity |
| 51 | ## Note |

### demo/demodata/pipelines/README.md

| Property | Value |
| --- | --- |
| Lines read | 82 |
| Nonblank lines | 65 |
| SHA-256 prefix | 67bea39b3773a571 |
| First line | # Pipeline Demo Data — MFS Fraud Detection Platform |
| Last line | ``` |
| Requirement-like lines | 4 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FRD-001, FRD-002, FRD-003, FRD-004, FRD-005, FRD-006, FRD-007, FRD-100, FRD-101, FRD-102, FRD-103, FRD-200, FRD-201, FRD-202, FRD-300, FRD-301, FRD-302, FRD-321 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Pipeline Demo Data — MFS Fraud Detection Platform |
| 5 | ## Domain |
| 13 | ## Organization Context |
| 17 | ### Teams & People |
| 30 | ### Infrastructure |
| 38 | ## Files |
| 57 | ## Cross-Reference Map |

### demo/script/walkthrough.md

| Property | Value |
| --- | --- |
| Lines read | 489 |
| Nonblank lines | 355 |
| SHA-256 prefix | 5f5f3e7254537a37 |
| First line | # EOIP Demo Walkthrough — Meridian Financial Services |
| Last line | - The 13 source system connectors each have their own JSON format validated by the platform |
| Requirement-like lines | 88 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen | FRD-001-008, FRD-100, FRD-200, FRD-300, FRD-321 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Demo Walkthrough — Meridian Financial Services |
| 12 | ## Prerequisites |
| 18 | ## Quick Setup |
| 21 | # From the repository root |
| 33 | ## Part 1: Health and Readiness (2 min) |
| 35 | ### 1.1 Verify services |
| 43 | ### 1.2 Check API docs |
| 49 | ## Part 2: Multi-Source Ingestion (5 min) |
| 53 | ### 2.1 Manual ingestion — Payment Gateway (PAY domain) |
| 78 | # Ingest Jira data (Payment Gateway) |
| 85 | ### 2.2 Pipeline ingestion — Fraud Detection (FRD domain) |
| 99 | ### 2.3 Run the automated demo |
| 102 | # Full demo — both domains + all capabilities |
| 105 | # Manual only (PAY domain) |
| 108 | # Pipeline only (FRD domain) |
| 114 | ## Part 3: Code-Graph Construction (3 min) |
| 116 | ### 3.1 Four MFS code repositories |
| 130 | ### 3.2 Explore code dependencies |
| 133 | # Search for the TokenizationService class |
| 137 | # Blast radius — what depends on TokenizationService? |
| 146 | ## Part 4: Crawler Data Processing (2 min) |
| 148 | ### 4.1 Five portal types crawled |
| 164 | ## Part 5: The Golden Evidence Path (5 min) |
| 168 | ### 5.1 Search for a work item |
| 178 | ### 5.2 Trace the full path |
| 181 | # Rally Epic → Jira Feature → Story → MR → Commit → File → CodeSymbol |
| 190 | ### 5.3 Path from story to code |
| 201 | ### 5.4 Impact analysis |
| 212 | ### 5.5 Incident root cause (INC0080101) |
| 215 | # Search for the payment timeout incident |
| 219 | # Explore its neighborhood |
| 232 | ## Part 6: AI-Assisted Analysis (5 min) |
| 234 | ### VS Code live segment (included in full auto-demo) |
| 249 | ### 6.1 RAG pattern routing (17 patterns) |
| 254 | # Simple RAG — entity lookup |
| 260 | # Multi-hop RAG — infrastructure to business impact |
| 266 | # Branched RAG — comparative analysis |
| 275 | ### 6.2 Agent dispatch (41 agent types, 9 categories) |
| 278 | # Compliance agent — PCI DSS verification |
| 284 | # Blast radius agent — dependency impact |
| 293 | ### 6.3 LAYA — Local AI Yield Augmentation (8 capabilities) |
| 296 | # Incident summary |
| 302 | # Release readiness |
| 315 | ## Part 7: Query Capabilities (3 min) |
| 317 | ### 7.1 Twelve query types |
| 334 | ### 7.2 Cross-domain query demo |
| 337 | # Which test cases in qTest cover the fraud scoring API endpoints? |
| 346 | ## Part 8: Administration (3 min) |
| 348 | ### 8.1 Admin panel |
| 357 | ### 8.2 Graph statistics |
| 366 | ### 8.3 Backup and restore |
| 377 | ## Part 9: Developer Integration (2 min) |
| 379 | ### 9.1 MCP tools |
| 383 | ### 9.2 VS Code extension |
| 390 | ### 9.3 Prometheus metrics |
| 400 | ## Cleanup |
| 408 | ## Quick Path (15 min version) |
| 422 | ## Key Entity Reference |
| 424 | ### Payment Gateway (Manual Folder — PAY Domain) |
| 442 | ### Fraud Detection (Pipeline Folder — FRD Domain) |
| 457 | ### People |
| 470 | ### Infrastructure |
| 482 | ## Honest Boundaries |

### docs/61-demo-playbook.md

| Property | Value |
| --- | --- |
| Lines read | 233 |
| Nonblank lines | 172 |
| SHA-256 prefix | 808a97917f3de213 |
| First line | # EOIP Demo Playbook |
| Last line | The graph and analytics are live application behavior over persisted demo data. The source exports are offline fixtures unless organization-specific connector URLs and credentials have been configured. Optional model synthesis is not required for any golden path. Native disaster recovery, full-scale production performance, and the remaining G2 P6-P10 roadmap items are not represented by this pack as completed capabilities. |
| Requirement-like lines | 74 |
| Status/gap/risk-like lines | 9 |
| Requirement IDs seen | EOIP-1, EOIP-2 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Demo Playbook |
| 7 | ## Prerequisites |
| 13 | ## 1. Clean environment start |
| 16 | # From the repository root |
| 30 | ## 2. Verify readiness |
| 38 | ## 3. Access the web application |
| 46 | ## 4. Demonstrate the evidence path |
| 50 | ### 4a. Search and explore |
| 56 | ### 4b. Trace a requirement to code |
| 62 | ### 4c. Run TraceImpact agent |
| 69 | ### 4d. Administration |
| 76 | ## 5. API demonstration |
| 79 | # Health check |
| 82 | # Search (requires Bearer token) |
| 85 | # Path query |
| 90 | # Impact analysis |
| 95 | # TraceImpact agent |
| 100 | # GraphRAG (deterministic fallback, no model required) |
| 105 | # Validation |
| 108 | # Ontology export (JSON-LD) |
| 112 | ## 6. MCP demonstration |
| 127 | ## 7. VS Code extension |
| 135 | ## 8. Backup and restore |
| 138 | # Create backup |
| 141 | # Run restore verification (separate HugeGraph instance) |
| 151 | ## 9. Run automated tests |
| 167 | ## 10. Clean reset |
| 171 | # Docker volumes are removed; next `up` starts fresh |
| 174 | ## Golden expectations |
| 187 | ## Enterprise sales scenarios |
| 209 | ### Suggested 20-minute pitch |
| 217 | ### Presenter API notes |
| 231 | ### Honest live-demo boundary |

### docs/adr-001-g2-contract-and-revision-model.md

| Property | Value |
| --- | --- |
| Lines read | 48 |
| Nonblank lines | 37 |
| SHA-256 prefix | 1afbc69c00c69abf |
| First line | # ADR-001: G2 source-event compatibility and revision model |
| Last line | audit middleware. |
| Requirement-like lines | 11 |
| Status/gap/risk-like lines | 1 |
| Requirement IDs seen | ADR-001, G2-ARCH-001..015, G2-EKAF-003, G2-EVENT-001, G2-EVOL-009 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # ADR-001: G2 source-event compatibility and revision model |
| 7 | ## Decision |
| 31 | ## Compatibility changes |
| 43 | ## Security and operations |

### docs/agents.md

| Property | Value |
| --- | --- |
| Lines read | 214 |
| Nonblank lines | 148 |
| SHA-256 prefix | 348a089528b2a552 |
| First line | # EOIP Agent Framework |
| Last line | ``` |
| Requirement-like lines | 27 |
| Status/gap/risk-like lines | 4 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Agent Framework |
| 7 | ## Agent Runtime (`packages/eoip/agents/runtime.py`) |
| 22 | ### Agent Contract (`packages/eoip/contracts/agent.py`) |
| 35 | ## Agent Catalog |
| 37 | ### Core Agents |
| 39 | #### TraceImpactAgent (`agents/trace_impact.py`) |
| 48 | #### BlastRadiusAgent (`agents/blast_radius.py`) |
| 55 | #### AnomalyDetectionAgent (`agents/anomaly.py`) |
| 61 | #### CommunityDetectionAgent (`agents/community.py`) |
| 67 | #### SimilarityAgent (`agents/similarity.py`) |
| 73 | #### TestCoverageAgent (`agents/test_coverage.py`) |
| 78 | #### IncidentCorrelationAgent (`agents/incident_correlation.py`) |
| 84 | #### CatalogAgent (`agents/catalog.py`) |
| 89 | #### FirewallAgent (`agents/firewall.py`) |
| 94 | #### EvaluationAgent (`agents/evaluation.py`) |
| 100 | #### GovernedAgent (`agents/governed.py`) |
| 107 | #### OrchestratorAgent (`agents/orchestration.py`) |
| 114 | #### ProposalAgent (`agents/proposals.py`) |
| 120 | ### Analytics Agents |
| 122 | #### GraphAnalyticsAgent (`agents/graph_analytics.py`) |
| 141 | #### SemanticIndexAgent (`agents/semantic_index.py`) |
| 153 | ### Support Agents |
| 155 | #### MemoryAgent (`agents/memory.py`) |
| 158 | #### AgentRouter (`agents/agent_router.py`) |
| 161 | #### TraceAgent (`agents/trace.py`) |
| 164 | #### KnowledgeDebtAgent (`agents/knowledge_debt.py`) |
| 169 | ## Tool Access Policy |
| 186 | ## Multi-Agent Orchestration |
| 201 | ## ExplanationEnvelope |

### docs/api-reference.md

| Property | Value |
| --- | --- |
| Lines read | 293 |
| Nonblank lines | 197 |
| SHA-256 prefix | fe2d74be22c15cf4 |
| First line | # EOIP API Reference |
| Last line | All tools are read-only. No mutation tools are exposed via MCP. |
| Requirement-like lines | 64 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP API Reference |
| 9 | ## Query Endpoints |
| 11 | ### `POST /api/v1/query` |
| 26 | ### `POST /api/v1/query/language` |
| 33 | ### `POST /api/v1/path` |
| 40 | ### `POST /api/v1/impact` |
| 47 | ### `POST /api/v1/search` |
| 54 | ### `POST /api/v1/nlq` |
| 63 | ## RAG & Retrieval |
| 65 | ### `POST /api/v1/rag` |
| 78 | ### `GET /api/v1/export/formats` |
| 81 | ### `GET /api/v1/ontology/export` |
| 90 | ## Graph Algorithms |
| 92 | ### `POST /api/v1/algorithms/run` |
| 102 | ### `GET /api/v1/algorithms` |
| 107 | ## Agent Endpoints |
| 109 | ### `POST /api/v1/agents/query` |
| 116 | ### `POST /api/v1/agents/analytics` |
| 128 | ### `POST /api/v1/agents/semantic-index` |
| 137 | ## Ingestion & Admin |
| 139 | ### `POST /api/v1/admin/ingestion/jira` |
| 146 | ### `POST /api/v1/admin/ingestion/confluence` |
| 153 | ### `POST /api/v1/admin/ingestion/servicenow` |
| 156 | ### `POST /api/v1/admin/ingestion/git` |
| 163 | ### `POST /api/v1/admin/semantic-pipeline` |
| 170 | ### `GET /api/v1/ingestion/runs` |
| 173 | ### `GET /api/v1/ingestion/dlq` |
| 176 | ### `POST /api/v1/admin/ingestion/replay` |
| 185 | ## Validation & Quality |
| 187 | ### `POST /api/v1/validation/run` |
| 192 | ### `GET /api/v1/validation/runs` |
| 195 | ### `GET /api/v1/quality` |
| 200 | ## Schema & Ontology |
| 202 | ### `GET /api/v1/ontology/schema` |
| 205 | ### `POST /api/v1/ontology/schema/generate` |
| 212 | ### `GET /api/v1/ontology/domains` |
| 217 | ## Lineage & Provenance |
| 219 | ### `POST /api/v1/lineage` |
| 226 | ### `POST /api/v1/evidence` |
| 235 | ## Admin Gremlin (Restricted) |
| 237 | ### `POST /api/v1/admin/gremlin` |
| 250 | ## Observability |
| 252 | ### `GET /metrics` |
| 258 | ### `GET /health/live` |
| 261 | ### `GET /health/ready` |
| 266 | ## Upload & File Ingestion |
| 268 | ### `POST /api/v1/upload` |
| 278 | ### `GET /api/v1/code/export` |
| 287 | ## VS Code / MCP Surfaces |

### docs/application-audit-2026-10-02.md

| Property | Value |
| --- | --- |
| Lines read | 76 |
| Nonblank lines | 57 |
| SHA-256 prefix | 351a4153a642b49a |
| First line | # EOIP application audit |
| Last line | Phase 1/MVP is the current implementation and acceptance boundary. Later roadmap items in `gaps-requirements.md`, `gaps2-requirements.md`, `gaps2-implementation.md`, and `knowgridflow-product-architecture.md` require new domain contracts, event/revision services, storage behavior, and acceptance tests before their GUI lenses can be truthfully enabled. They must not be represented as completed merely through placeholder screens. |
| Requirement-like lines | 36 |
| Status/gap/risk-like lines | 4 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP application audit |
| 17 | ## Executive result |
| 23 | ## Requirement-to-implementation audit |
| 36 | ## GUI audit and implemented closure |
| 57 | ## Code-quality findings closed |
| 63 | ## Verification evidence |
| 74 | ## Honest completion boundary |

### docs/audit-2026-10-06/assessed-gap-report.md

| Property | Value |
| --- | --- |
| Lines read | 712 |
| Nonblank lines | 578 |
| SHA-256 prefix | 001c9ca30ba24bcc |
| First line | # EOIP Assessed Gap Report |
| Last line | *Pass 8 final - 2026-10-07. Full GAP gate closure with enterprise completion contracts, updated coverage tests, focused regression, and updated detailed audit deliverables. Supersedes all prior audit files in this directory.* |
| Requirement-like lines | 241 |
| Status/gap/risk-like lines | 262 |
| Requirement IDs seen | FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020, FR-021, FR-022, FR-023, FR-024, FR-025, FR-026, FR-027, FR-028, FR-ADMIN-001, FR-ADMIN-002, FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, FR-CODE-001, FR-CODE-002, FR-CODE-003, FR-CODE-004, FR-CODE-005 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Assessed Gap Report |
| 12 | ## Executive Summary |
| 52 | ### Repository-wide Markdown Audit Addendum (2026-10-06) |
| 77 | ## 0. Audit History and Consolidation |
| 79 | ### 0.1 Audit File Provenance |
| 93 | ### 0.2 Policy Reconciliation |
| 97 | ### 0.3 Pass 5 New Findings |
| 111 | ### 0.4 Repository Documentation Reconciliation |
| 125 | ## 1. Core Functional Requirements |
| 127 | ### 1.1 Connectors (FR-CONN) |
| 141 | ### 1.2 Ingestion (FR-INGEST) |
| 151 | ### 1.3 Graph Core (FR-GRAPH) |
| 168 | ### 1.4 Ontology / Provenance / Identity / Temporal |
| 180 | ### 1.5 Code Graph (FR-CODE) |
| 190 | ### 1.6 Query Engine (FR-QUERY) |
| 203 | ### 1.7 Validation (FR-VALID) |
| 211 | ### 1.8 RAG (FR-RAG) |
| 222 | ### 1.9 Agents (FR-AGENT) |
| 232 | ### 1.10 Memory / MCP / UI / Admin / VS Code |
| 248 | ## 2. Non-Functional Requirements |
| 269 | ## 3. Previously Partial/Missing Items â€” ALL RESOLVED |
| 286 | ## 4. Query Language & Format Support |
| 288 | ### 4.1 Core Query Languages (12 formats) |
| 305 | ### 4.2 Phase C Extensions |
| 320 | ## 5. Graph Algorithms (30+ Total) |
| 322 | ### 5.1 Core Algorithms |
| 350 | ### 5.2 Phase C Extended Algorithms (`graph/algorithms.py`) |
| 371 | ## 6. Semantic Indexing Pipeline |
| 388 | ## 7. Agent Catalog (20 Agents) |
| 419 | ## 8. GAPS Phase 0-1 Implementation Status |
| 421 | ### 8.1 Implemented (37 items Done) |
| 436 | ### 8.2 Pass 6 Closed Challenge Items (8 items) |
| 449 | ### 8.3 Pass 5 New: Federation Planner (GAP-FABRIC-001..008) |
| 462 | ### 8.4 Pass 5 New: Ops Preflight (GAP-OPS-001) |
| 468 | ### 8.5 Pass 7 New: Future Scope Slices 1-2 (47 items) |
| 489 | ### 8.6 Pass 8 New: Full GAP Gate Closure (181 audit-gate blockers) |
| 508 | ## 9. GAPS2 All Phases P0-P10 â€” Full Coverage Rerun |
| 513 | ### 9.1 G2 Coverage by Phase (Automated Scan + Pass 6 Closure) |
| 531 | ### 9.2 Pass 6 Closed Challenge Items (12 items) |
| 550 | ## 10. Pass 5 New: Multi-Backend GraphStore |
| 554 | ### 10.1 Backend Registry |
| 563 | ### 10.2 Configuration |
| 587 | ## 11. Test Coverage (Verified 2026-10-06, Pass 6 Final) |
| 589 | ### 11.1 Test Suite Summary |
| 600 | ### 11.2 Latest Test Run Results |
| 609 | ### 11.3 New Tests Added (Pass 4 + Pass 5 + Pass 6) |
| 628 | ### 11.4 Live Integration Evidence |
| 638 | ## 12. MVP Requirements (28/28 Done) |
| 673 | ## 13. Documentation Inventory (Pass 5 + Pass 6) |
| 694 | ## 14. Known Constraints and Limitations |

### docs/audit-2026-10-06/detailed-requirements-report.md

| Property | Value |
| --- | --- |
| Lines read | 57 |
| Nonblank lines | 46 |
| SHA-256 prefix | 82b0ce6403cdf2f0 |
| First line | # EOIP Detailed Requirements Report |
| Last line | \| Security certification \| External gate \| Local security tests exist; formal penetration/compliance certification is outside this repository pass. \| |
| Requirement-like lines | 14 |
| Status/gap/risk-like lines | 21 |
| Requirement IDs seen | GAP-AGOV-001..005, GAP-AKO-001..010, GAP-ARCH-001..006, GAP-CHANGE-001..006, GAP-CONTRACT-001..006, GAP-CP-001..008, GAP-DBAGNOSTIC-001, GAP-EXPORT-001, GAP-HG-001..010, GAP-KQ-001..006, GAP-KRAG-001..010, GAP-NOCODE-001..003, GAP-OFFLINE-001, GAP-PORT-001, GAP-PROV-005, GAP-RET-001..006, GAP-SDT-001..008, GAP-STUDIO-001..011 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Detailed Requirements Report |
| 7 | ## Audit Position |
| 21 | ## Gap Closure Table |
| 39 | ## Verification |
| 50 | ## Realistic Constraints |

### docs/audit-2026-10-06/phase-by-phase-implementation-approach.md

| Property | Value |
| --- | --- |
| Lines read | 51 |
| Nonblank lines | 41 |
| SHA-256 prefix | a6bf00de05eda563 |
| First line | # EOIP Phase-by-Phase Implementation Approach |
| Last line | \| New enterprise completion tests \| 4 passed \| |
| Requirement-like lines | 20 |
| Status/gap/risk-like lines | 15 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Phase-by-Phase Implementation Approach |
| 6 | ## Implementation Status |
| 22 | ## Remaining Execution Plan |
| 35 | ## Acceptance Policy |
| 43 | ## Latest Verification |

### docs/benchmarking.md

| Property | Value |
| --- | --- |
| Lines read | 105 |
| Nonblank lines | 82 |
| SHA-256 prefix | 15ebeb27a54285f8 |
| First line | # EOIP benchmark guide |
| Last line | index. Index replacement preserves graph data. |
| Requirement-like lines | 12 |
| Status/gap/risk-like lines | 1 |
| Requirement IDs seen | NFR-PERF-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP benchmark guide |
| 8 | ## Profiles |
| 20 | ## Commands |
| 49 | ## Published 2026-10-03 evidence |
| 87 | ## Remaining acceptance evidence |

### docs/code-graph.md

| Property | Value |
| --- | --- |
| Lines read | 198 |
| Nonblank lines | 148 |
| SHA-256 prefix | 6e54f21cf9e13494 |
| First line | # EOIP Code Graph |
| Last line | Uses `TraceLineageAgent` to follow the chain: `TestCase → COVERS → CodeSymbol`. |
| Requirement-like lines | 14 |
| Status/gap/risk-like lines | 1 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Code Graph |
| 7 | ## Overview |
| 23 | ## Code Parser (`packages/eoip/codegraph/parser.py`) |
| 27 | ### Supported Languages |
| 34 | ### Symbol Kinds |
| 37 | ### `parse(repo_id, path, source) → ParseResult` |
| 48 | ## SymbolRange (`packages/eoip/codegraph/parser.py`) |
| 64 | ## DiffHunk (`packages/eoip/codegraph/diff_hunk.py`) |
| 82 | ## CommitSymbolLink (`packages/eoip/codegraph/link.py`) |
| 95 | ## Code Graph JSON Format |
| 132 | ## Code Graph API |
| 134 | ### Export |
| 140 | ### Search |
| 146 | ### Impact from Symbol |
| 152 | ### Symbol → Test Coverage |
| 160 | ## Cross-Domain Links |
| 174 | ## MCP Tools for Code Graph |
| 189 | ## TestCoverageAgent |

### docs/connectors-github.md

| Property | Value |
| --- | --- |
| Lines read | 85 |
| Nonblank lines | 70 |
| SHA-256 prefix | 19d971d6a082e7fe |
| First line | # GitHub connector |
| Last line | - https://docs.github.com/en/rest/authentication/permissions-required-for-github-apps |
| Requirement-like lines | 12 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # GitHub connector |
| 7 | ## Supported surface |
| 20 | ## Minimum access |
| 26 | ## Registry example |
| 66 | ## Webhooks |
| 73 | ## Safety limits |

### docs/connectors-gitlab.md

| Property | Value |
| --- | --- |
| Lines read | 109 |
| Nonblank lines | 95 |
| SHA-256 prefix | 11c2dbe114b85660 |
| First line | # GitLab connector |
| Last line | - https://docs.gitlab.com/user/project/pages/ |
| Requirement-like lines | 15 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # GitLab connector |
| 7 | ## Supported surface |
| 23 | ## Registry example |
| 73 | ## Webhooks |
| 88 | ## Safety and operational limits |

### docs/connectors.md

| Property | Value |
| --- | --- |
| Lines read | 193 |
| Nonblank lines | 149 |
| SHA-256 prefix | 023fcb1c0490c6c6 |
| First line | # EOIP Source Connectors |
| Last line | Credentials are **never** included in API payloads or job records. |
| Requirement-like lines | 37 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Source Connectors |
| 5 | ## Connector Protocol |
| 18 | ## Connector Infrastructure |
| 30 | ## Source Connectors (24) |
| 32 | ### Work Management |
| 34 | #### Jira (`connectors/jira.py` + `connectors/jira_json.py`) |
| 41 | #### Rally (`connectors/rally.py`) |
| 46 | #### qTest (`connectors/qtest.py`) |
| 51 | ### Source Control & CI/CD |
| 53 | #### GitLab (`connectors/gitlab.py` + `connectors/gitlab_json.py`) |
| 59 | #### GitHub (`connectors/github.py`) |
| 65 | #### Local Code (`connectors/local_code.py`) |
| 71 | #### CI/CD (`connectors/cicd.py`) |
| 77 | ### Documentation & Knowledge |
| 79 | #### Confluence (`connectors/confluence.py` + `confluence_body.py` + `confluence_metadata.py`) |
| 87 | #### ServiceNow (`connectors/servicenow.py`) |
| 93 | #### Web Crawler (`connectors/crawler.py`) |
| 99 | #### Generic (`connectors/generic.py`) |
| 104 | ### Observability & Monitoring |
| 106 | #### Datadog (`connectors/datadog.py`) |
| 110 | #### Grafana (`connectors/grafana.py`) |
| 114 | #### Kibana (`connectors/kibana.py`) |
| 118 | ### Design & API |
| 120 | #### Figma (`connectors/figma.py`) |
| 124 | #### API Portal (`connectors/api_portal.py`) |
| 128 | ### Security & Infrastructure |
| 130 | #### SBOM/SCA (`connectors/sbom.py`) |
| 136 | #### OpenTelemetry (`connectors/otel.py`) |
| 142 | #### Runtime Infrastructure (`connectors/runtime_infra.py`) |
| 147 | ### File & Upload |
| 149 | #### Files (`connectors/files.py`) |
| 154 | #### Webhook (`connectors/webhook.py`) |
| 161 | ## Adding a New Connector |
| 177 | ## Connector Configuration |

### docs/deep-agents-xai.md

| Property | Value |
| --- | --- |
| Lines read | 55 |
| Nonblank lines | 34 |
| SHA-256 prefix | dccf5e87c524afc4 |
| First line | # Governed Deep Agents and XAI |
| Last line | Set `enabled: false` in a deployed agent contract to stop new runs. The runtime fails closed for unknown or disabled agents, unregistered tools, exhausted budgets, open circuit breakers, and missing approvals. Trace files are written atomically under `${EOIP_DATA_DIR}/agent-traces`; audit events and the graph `AgentRun` record retain actor and correlation identifiers without source payloads or hidden reasoning. |
| Requirement-like lines | 17 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Governed Deep Agents and XAI |
| 5 | ## Implemented agent catalog |
| 11 | ## Execution lifecycle |
| 21 | ## Explainability contract |
| 35 | ## APIs |
| 47 | ## Orchestration and release evaluation |
| 53 | ## Operational controls |

### docs/demo-readiness-audit-2026-10-03.md

| Property | Value |
| --- | --- |
| Lines read | 178 |
| Nonblank lines | 148 |
| SHA-256 prefix | dd56654c7f860ee7 |
| First line | # EOIP enterprise demo-readiness audit |
| Last line | - The desktop in-app browser runtime exposed no controllable browser instance during this audit. Visual verification was therefore completed through the repository's Dockerized Playwright/Chromium suite rather than an interactive browser session. |
| Requirement-like lines | 70 |
| Status/gap/risk-like lines | 18 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP enterprise demo-readiness audit |
| 7 | ## Audit inventory and method |
| 9 | ### Current enterprise remediation progress |
| 86 | ## Executive finding |
| 101 | ## Capability reconciliation |
| 117 | ## Scenario acceptance matrix |
| 130 | ## Data and schema controls |
| 136 | ## Remaining gaps and sales claims to avoid |
| 147 | ## Release gate |
| 161 | ## Historical verification executed on 2026-10-04 |

### docs/deployment-ha.md

| Property | Value |
| --- | --- |
| Lines read | 139 |
| Nonblank lines | 115 |
| SHA-256 prefix | 3ea59455ba114a50 |
| First line | # EOIP High-Availability Deployment |
| Last line | (GAP-HG-008) before production. |
| Requirement-like lines | 35 |
| Status/gap/risk-like lines | 7 |
| Requirement IDs seen | GAP-HG-004, GAP-HG-006, GAP-HG-008, GAP-PERF-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP High-Availability Deployment |
| 9 | ## Topology |
| 38 | ## Compose HA profile |
| 41 | # from deploy/ — .env via scripts/docker.ps1 |
| 50 | ## Helm |
| 70 | ## RPO / RTO targets |
| 79 | ## Rolling restart procedure |
| 90 | ## Capacity planning |
| 100 | ## Failure scenarios |
| 113 | ## Standalone → distributed HugeGraph migration (GAP-HG-006) |
| 126 | ## HugeGraph cluster / sharding notes (GAP-PERF-001/002, G2-SCALE-SHARD) |

### docs/deployment-verification.md

| Property | Value |
| --- | --- |
| Lines read | 35 |
| Nonblank lines | 31 |
| SHA-256 prefix | b41441c81d4d43fe |
| First line | # Local deployment verification |
| Last line | graph and test runners were removed. No Git commit was created. |
| Requirement-like lines | 19 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Local deployment verification |

### docs/docker-local.md

| Property | Value |
| --- | --- |
| Lines read | 748 |
| Nonblank lines | 641 |
| SHA-256 prefix | bba8d1b6778f346f |
| First line | # Local Docker deployment |
| Last line | [edge REST API](https://hugegraph.apache.org/docs/clients/restful-api/edge/). |
| Requirement-like lines | 231 |
| Status/gap/risk-like lines | 23 |
| Requirement IDs seen | EOIP-1 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Local Docker deployment |
| 8 | ## Start and connect |
| 54 | ## Services and storage |
| 86 | ### Schema compatibility and startup refusal |
| 112 | ## Exercise the demo |
| 129 | ## Confluence and ServiceNow ingestion |
| 153 | ## Automated checks |
| 180 | ### Fresh demo and recovery acceptance |
| 240 | ## Isolated live DLQ/API/worker acceptance |
| 340 | ## Bounded scoped agent task memory |
| 391 | ### Confluence storage extraction boundaries |
| 409 | ### Confluence source metadata boundaries |
| 439 | ### Confluence history, document links and freshness boundaries |
| 485 | ## Backup and restore |
| 565 | ### Self-contained configuration and model-weight bundles |
| 653 | ## Executable MVP requirement evidence |
| 692 | ## VS Code extension |
| 705 | ## Optional local generation and metrics |
| 726 | ## Implementation boundaries |

### docs/eoip-development-audit-2026-10-03.md

| Property | Value |
| --- | --- |
| Lines read | 563 |
| Nonblank lines | 481 |
| SHA-256 prefix | 74411c7ce969e82d |
| First line | # EOIP Development and Demo-Readiness Audit |
| Last line | performance claim. |
| Requirement-like lines | 256 |
| Status/gap/risk-like lines | 85 |
| Requirement IDs seen | EOIP-1, FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020, FR-021, FR-022, FR-023, FR-024, FR-025, FR-026, FR-027, FR-028, FR-ADMIN-001, FR-ADMIN-002, FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, FR-CODE-001, FR-CODE-002, FR-CODE-003, FR-CODE-004 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Development and Demo-Readiness Audit |
| 9 | ## Remediation update — 2026-10-03 |
| 11 | ### Superseding demo evidence — 2026-10-04 |
| 22 | ### Latest release-operations evidence |
| 69 | ### Priority gate 2 — Docker demo stack |
| 83 | ### Priority gate 3 — repeat ingestion, smoke, and browser acceptance |
| 96 | ## 1. Summary |
| 118 | ### How to read the estimates |
| 130 | ## 2. Repository inventory and counting method |
| 132 | ### 2.1 Included workspace file categories |
| 151 | ### 2.2 Code LOC |
| 161 | ### 2.3 Markdown counts |
| 175 | ## 3. Current validation and readiness evidence |
| 190 | ## 4. Requirement and feature completion |
| 192 | ### 4.1 P1/MVP acceptance criteria: all 28 |
| 229 | ### 4.2 Normative functional requirements: all 67 unique `FR-*` |
| 305 | ### 4.3 Non-functional requirements: all 14 |
| 328 | ### 4.4 Implementation task register: 82 distinct `WP-*` |
| 421 | ## 5. Prioritized completion sequence |
| 439 | ## 6. Phase-level assessment |
| 451 | ## 7. Scope, ambiguities, and audit limitations |
| 461 | ## 8. Evidence and source references |
| 463 | ### Normative engineering package |
| 472 | ### Current implementation and validation references |
| 486 | ### Current commands/results referenced |
| 496 | ## 9. Sign-off |
| 501 | ## 10. Continuation remediation evidence (revision `354b8a9` plus working changes) |
| 506 | ### Clean deployment and recovery gates |
| 524 | ### `NFR-PERF-001` benchmark package |

### docs/file-parsing.md

| Property | Value |
| --- | --- |
| Lines read | 195 |
| Nonblank lines | 160 |
| SHA-256 prefix | 135dc56618bb8f9e |
| First line | # Actual file parsing and ingestion |
| Last line | RAR and Linux image/HugeGraph execution need environment-specific verification. |
| Requirement-like lines | 28 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Actual file parsing and ingestion |
| 7 | ## Installation and format support |
| 61 | ## CLI and Python |
| 82 | ## Artifact contract |
| 108 | ## Authenticated raw upload API |
| 140 | ## Registered sources and replay |
| 176 | ## Limits and failures |

### docs/g2-traceability.md

| Property | Value |
| --- | --- |
| Lines read | 64 |
| Nonblank lines | 61 |
| SHA-256 prefix | 511116e6579f367b |
| First line | # G2 implementation traceability |
| Last line | use synthetic fixtures and must not be reported as a successful live integration. |
| Requirement-like lines | 42 |
| Status/gap/risk-like lines | 55 |
| Requirement IDs seen | G2-ARCH-001..015, G2-EKAF-003, G2-EKAF-017, G2-EKAF-018, G2-EKAF-022, G2-KD-001..006, G2-OBS-001..006, G2-QOP-001, G2-QOP-003, G2-QOP-004, G2-REQ-34, G2-SIM-001..007, G2-SLO-001..005, GAP-GRAPHTEST-001..011, GAP-KP-001..005, GAP-RET-002, GAP-RET-003, GAP-RET-006, GAP-SEARCH-001..002, GAP-STUDIO-005, GAP-TAX-001, GAP-TEMP-001..005, GAP-TRUTH-001..010 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # G2 implementation traceability |

### docs/gap-audit-2026-10-02.md

| Property | Value |
| --- | --- |
| Lines read | 637 |
| Nonblank lines | 557 |
| SHA-256 prefix | 988d4d87d59f3927 |
| First line | # EOIP implementation gap audit & prioritized backlog |
| Last line | - Live API validation — health/search/query/path/impact/lineage/ingestion-runs/rag/web all green. |
| Requirement-like lines | 168 |
| Status/gap/risk-like lines | 31 |
| Requirement IDs seen | EOIP-1, FR-002, FR-013, FR-AGENT-001, FR-CODE-003, FR-CONF-001, FR-CONN-001, FR-CONN-003, FR-CONN-006, FR-CONN-007, FR-GRAPH-002, FR-GRAPH-003, FR-GRAPH-009, FR-ID-001, FR-INGEST-002, FR-INGEST-003, FR-INGEST-005, FR-MCP-001, FR-MEM-001, FR-QUERY-003, FR-QUERY-004, FR-QUERY-005, FR-RAG-005, FR-SNOW-001, FR-VALID-002, FR-VALID-003, G2-SRC-CONF-001, G2-SRC-CONF-002, G2-SRC-CONF-003, G2-SRC-CONF-004, NFR-PERF-001, NFR-PRIV-001, NFR-REL-002, NFR-SEC-001, NFR-SEC-007, WP-AGENT-MEMORY-06, WP-EXPERIENCE-06 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP implementation gap audit & prioritized backlog |
| 8 | ## Temporal upgrade compatibility follow-up - 2026-10-04 |
| 49 | ## Original status summary (2026-10-02; historical) |
| 65 | ## Implementation progress — 2026-10-03 |
| 78 | ## Reconciliation and implementation batch - 2026-10-03 |
| 99 | ### Recovery and executable requirement evidence - 2026-10-04 |
| 158 | ### Scoped task-memory certification |
| 197 | ### Current operational-recovery certification |
| 233 | ### Gap 22: schema compatibility |
| 263 | ### Gap 19: canonical ingestion boundary |
| 316 | ### Next completion order |
| 327 | ### Confluence history, reference freshness and temporal recovery certification |
| 371 | ### Registered SourceEvent v2 replay acceptance - 2026-10-03 |
| 395 | ### ServiceNow acquisition and replay admission - 2026-10-03 |
| 421 | ### Confluence HTTP acquisition and provenance repair - 2026-10-03 |
| 457 | ### Confluence structured body extraction - 2026-10-03 |
| 487 | ### Confluence labels, author/editor and timestamps - 2026-10-03 |
| 517 | ### Live DLQ/API/worker acceptance - 2026-10-03 |
| 550 | ### Real VS Code host command acceptance (2026-10-03) |
| 577 | ## P0 — blocks MVP acceptance (fix first) |
| 586 | ## P1 — required by P1-MVP docs |
| 606 | ## Web app |
| 618 | ## VS Code extension |
| 625 | ## G2 roadmap (phase-by-phase, after P0/P1) |
| 633 | ## Verification baseline |

### docs/graph-algorithms.md

| Property | Value |
| --- | --- |
| Lines read | 210 |
| Nonblank lines | 144 |
| SHA-256 prefix | 11eaaeba82fcd2a4 |
| First line | # EOIP Graph Algorithms |
| Last line | Tests: `tests/unit/test_graph_metrics.py`, `tests/unit/test_graph_algorithms.py`, `tests/unit/test_community_detection.py` |
| Requirement-like lines | 16 |
| Status/gap/risk-like lines | 1 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Graph Algorithms |
| 7 | ## Module Map |
| 19 | ## Centrality (`metrics.py`) |
| 21 | ### `CentralityMetrics` |
| 41 | ### `BlastRadiusResult` |
| 50 | ### What-If Analysis |
| 58 | ## Path Algorithms (`paths.py`) |
| 60 | ### BFS Path |
| 63 | ### Dijkstra / Weighted Shortest Path |
| 66 | ### K-Shortest Paths (Yen's algorithm) |
| 69 | ### Bi-Directional BFS |
| 72 | ### All Simple Paths |
| 77 | ## Similarity Algorithms (`similarity.py`) |
| 79 | ### Jaccard Similarity |
| 82 | ### Adamic-Adar |
| 85 | ### Common Neighbors |
| 88 | ### SimRank |
| 93 | ## Community Detection (`community.py`) |
| 95 | ### Louvain Modularity |
| 100 | ### Label Propagation |
| 103 | ### K-Core Decomposition |
| 108 | ## Extended Algorithms (`algorithms.py`) |
| 110 | ### Cycle / Ring Detection |
| 115 | ### K-Step Neighborhood |
| 118 | ### Co-Neighbor Analysis |
| 121 | ### Subgraph Intersection |
| 126 | ### Directional Ray Traversal |
| 131 | ### Weighted Path (Dijkstra) |
| 134 | ### Recommendations |
| 137 | ### Temporal Degree Sequence |
| 142 | ## Process Mining Algorithms |
| 156 | ## Phase C Extended Algorithms (12) |
| 177 | ## GraphAnalyticsAgent Swarm Mode |
| 194 | ## API Usage |

### docs/hubble-local.md

| Property | Value |
| --- | --- |
| Lines read | 224 |
| Nonblank lines | 181 |
| SHA-256 prefix | 2b4bb14ee5414b6c |
| First line | # Hubble Basics + standalone RocksDB |
| Last line | applied to this pinned release. |
| Requirement-like lines | 64 |
| Status/gap/risk-like lines | 6 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Hubble Basics + standalone RocksDB |
| 7 | ## Start, credentials and URL |
| 59 | ## View and query actual ingested data |
| 114 | ## Load all available demonstration data |
| 149 | ### Verified local corpus receipt |
| 165 | ## Data-safe clean builds |
| 203 | ## Validation |

### docs/hubble-runtime-validation.md

| Property | Value |
| --- | --- |
| Lines read | 441 |
| Nonblank lines | 379 |
| SHA-256 prefix | 81ce2c1021bafe9b |
| First line | # Hubble Runtime Validation Report |
| Last line | separately approved volume deletion. Keep the Compose project name `eoip`. |
| Requirement-like lines | 73 |
| Status/gap/risk-like lines | 24 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Hubble Runtime Validation Report |
| 9 | ## Summary |
| 11 | ### Current remediation checkpoint |
| 111 | ### Latest validation verdict |
| 129 | ### Code-export import contract |
| 148 | ## Historical verification |
| 154 | ### Historical 1.1.0 acceptance |
| 184 | ## Historical environment and verdict |
| 213 | ## Historical 1.1.0 acceptance checklist |
| 235 | ## Historical 1.1.0 enterprise enrichment evidence |
| 298 | ## Historical corpus and persistence evidence |
| 339 | ## Test commands and scope |
| 390 | ### Browser changes |
| 398 | ## Historical twelve-failure regression |
| 424 | ## Manual use |

### docs/ingestion.md

| Property | Value |
| --- | --- |
| Lines read | 239 |
| Nonblank lines | 170 |
| SHA-256 prefix | b0379195968be509 |
| First line | # EOIP Ingestion Pipeline |
| Last line | API: `POST /api/v1/upload` |
| Requirement-like lines | 42 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Ingestion Pipeline |
| 7 | ## Pipeline Stages |
| 25 | ## Ingestion Services |
| 49 | ## Validated Write Boundary (`ingestion/pipeline.py`) |
| 68 | ## GraphEvolutionEngine |
| 91 | ## Dead-Letter Queue (`ingestion/dlq.py`) |
| 106 | ### DLQ Replay (`ingestion/replay.py`) |
| 118 | ## Checkpointing |
| 126 | ## Jira Ingestion (`ingestion/jira.py`) |
| 128 | ### Fixture Mode (JSON) |
| 134 | ### Live Mode |
| 143 | ## GitLab Ingestion (`ingestion/gitlab.py`) |
| 151 | ## Code Ingestion (`ingestion/code.py`) |
| 164 | ## Code Graph JSON Ingestion (`ingestion/code_graph_json.py`) |
| 181 | ## Semantic Pipeline (`ingestion/semantic_pipeline.py`) |
| 205 | ## Ingestion Run Tracking |
| 224 | ## File Ingestion (`ingestion/files.py`) |

### docs/ontology.md

| Property | Value |
| --- | --- |
| Lines read | 249 |
| Nonblank lines | 189 |
| SHA-256 prefix | e8ecb9fd3244f1cc |
| First line | # EOIP Ontology |
| Last line | If HugeGraph is unavailable, the system falls back to `MemoryGraphStore` (in-memory dict-based store) for local dev. |
| Requirement-like lines | 41 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Ontology |
| 11 | ## Graph Domains (14) |
| 34 | ## Vertex Labels (50+) |
| 36 | ### META Domain |
| 51 | ### WORK Domain |
| 67 | ### CODE Domain |
| 82 | ### CICD Domain |
| 93 | ### OPS Domain |
| 105 | ### Other Domains (TEST, DESIGN, KNOWLEDGE, IDENTITY, etc.) |
| 110 | ## Edge Labels (30+) |
| 140 | ## Canonical ID Format |
| 159 | ## Schema Generation (`packages/eoip/ontology/schema_gen.py`) |
| 176 | ## SKOS Export (`packages/eoip/ontology/skos.py`) |
| 188 | ## RDF / JSON-LD Export (`packages/eoip/ontology/rdf.py`) |
| 199 | ## Ontology Packs (`packages/eoip/ontology/packs.py`) |
| 205 | # Includes: Repository, File, CodeSymbol, Commit, Dependency, Service, ... |
| 210 | ## Embedding Drift Detection (`packages/eoip/ontology/embedding_drift.py`) |
| 222 | ## Ontology Drift (`packages/eoip/ontology/drift.py`) |
| 231 | ## GitOps Integration (`packages/eoip/ontology/gitops.py`) |
| 240 | ## HugeGraph Schema Bootstrap |

### docs/phase-completion-audit-2026-10-03.md

| Property | Value |
| --- | --- |
| Lines read | 400 |
| Nonblank lines | 364 |
| SHA-256 prefix | 1d800705701bf92f |
| First line | # EOIP/KnowGridFlow — Phase Completion Audit Checklist |
| Last line | 17 read-only tools; web app HTTP 200. |
| Requirement-like lines | 126 |
| Status/gap/risk-like lines | 31 |
| Requirement IDs seen | ADR-001, EOIP-1, FR-CONF-001, FR-MEM-001, G2-REL-006, G2-SRC-CONF-001, G2-SRC-CONF-002, G2-SRC-CONF-003, NFR-KGR-005, WP-AGENT-MEMORY-06 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP/KnowGridFlow — Phase Completion Audit Checklist |
| 6 | ## Latest bounded certification - 2026-10-04 |
| 276 | ## Phase 1 / MVP (T01–T28) — IMPLEMENTED |
| 292 | ## Gap-closure items from the 2026-10-02 audit — status |
| 341 | ## G2 / KnowGridFlow phases |
| 357 | ## KGR (Knowledge Graph Renderer & Explorer) — phases 1–8 IMPLEMENTED |
| 363 | ## Honest completion boundary |
| 367 | ## Final integration certification — 2026-10-04 (this pass) |

### docs/query-engine.md

| Property | Value |
| --- | --- |
| Lines read | 220 |
| Nonblank lines | 156 |
| SHA-256 prefix | 8b9eb7c9596ae1a8 |
| First line | # EOIP Query Engine |
| Last line | API: `GET /api/v1/export/formats`, `GET /api/v1/ontology/export` |
| Requirement-like lines | 13 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Query Engine |
| 7 | ## Query Languages |
| 20 | ## EQL — EOIP Query Language |
| 49 | ## NLQ — Natural Language Query |
| 69 | ## EOQL — Enterprise Object Query Language |
| 93 | ## OSQL — Ontology SQL |
| 111 | ## Semantic Query Language |
| 132 | ## QueryPlan Executor (`packages/eoip/query/executor.py`) |
| 134 | ### QueryPlan (`packages/eoip/contracts/query_plan.py`) |
| 146 | ### Intent Dispatch |
| 156 | ### GraphResult |
| 170 | ## Query Safety Policy (`packages/eoip/query/policy.py`) |
| 187 | ## Parameterized Gremlin Templates |
| 199 | ## Export Formats |

### docs/rag.md

| Property | Value |
| --- | --- |
| Lines read | 196 |
| Nonblank lines | 138 |
| SHA-256 prefix | 3e2d4d4fdc38ad45 |
| First line | # EOIP GraphRAG Retrieval System |
| Last line | Tests: `tests/unit/test_retrieval.py` |
| Requirement-like lines | 24 |
| Status/gap/risk-like lines | 1 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP GraphRAG Retrieval System |
| 7 | ## Architecture Overview |
| 25 | ## Retrieval Service (`packages/eoip/retrieval/service.py`) |
| 27 | ### `retrieve(question, strategy, context)` |
| 30 | ### Model-Down Fallback |
| 40 | ## RAGRouter (`packages/eoip/graph/rag_router.py`) |
| 58 | ## Retrieval Strategies |
| 60 | ### GRAPH |
| 65 | ### KEYWORD |
| 70 | ### HYBRID |
| 73 | ### SEMANTIC |
| 78 | ### EVIDENCE |
| 83 | ### LINEAGE |
| 88 | ### AGENT |
| 95 | ## Strategy Registry (`packages/eoip/retrieval/strategy_registry.py`) |
| 99 | ### RAGStrategyPlugin Protocol |
| 110 | ### StrategyPhase |
| 113 | ### StrategyRegistry |
| 121 | ### Built-in Strategies (4) |
| 134 | ## Vector Search (No Vector DB Required) |
| 146 | ## Local Model Abstraction (`packages/eoip/models/provider.py`) |
| 161 | ## Evidence Citations (`packages/eoip/contracts/retrieval.py`) |
| 182 | ## RAG Evaluation (`packages/eoip/retrieval/eval.py`) |

### docs/validation-evidence-phase1.md

| Property | Value |
| --- | --- |
| Lines read | 92 |
| Nonblank lines | 73 |
| SHA-256 prefix | 80072c222615f24c |
| First line | # Audit phase 1: validation evidence foundation |
| Last line | Completed by assumption. |
| Requirement-like lines | 19 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-027 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Audit phase 1: validation evidence foundation |
| 3 | ## Scope and acceptance |
| 19 | ## Author-executed checks |
| 65 | ## Coverage and limitations |
| 86 | ## Review stop |

### EOIP-engg-doc-pkg/00-specification-audit-and-enhancements.md

| Property | Value |
| --- | --- |
| Lines read | 108 |
| Nonblank lines | 88 |
| SHA-256 prefix | 4084401be2f9b048 |
| First line | # Specification Audit and Requirement Enhancements |
| Last line | Initial engineering targets are acceptance thresholds to validate after implementation: indexed entity lookup p95 ≤ 500 ms; bounded path/impact query p95 ≤ 2 s at configured depth/result limits; standard user API p95 ≤ 1 s excluding local-model generation; `docker compose up` readiness ≤ 120 s after images are locally available. These are not product performance claims until the benchmark suite measures them. |
| Requirement-like lines | 43 |
| Status/gap/risk-like lines | 5 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Specification Audit and Requirement Enhancements |
| 11 | ## Executive assessment |
| 15 | ## Ambiguities, conflicts and resolutions |
| 36 | ## Missing requirements added |
| 54 | ## Conflict hierarchy |
| 65 | ## MVP architecture after enhancement |
| 90 | ## Phase 1 security baseline |
| 104 | ## MVP benchmark definition (targets, not measured claims) |

### EOIP-engg-doc-pkg/01-project-vision.md

| Property | Value |
| --- | --- |
| Lines read | 42 |
| Nonblank lines | 30 |
| SHA-256 prefix | a9f4126e7cda138e |
| First line | # Project Vision |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 12 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-GRAPH-001, FR-GRAPH-006, FR-PROV-001, FR-QUERY-003, FR-RAG-002 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Project Vision |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 28 | ## Engineering rules |
| 36 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/02-scope-and-objectives.md

| Property | Value |
| --- | --- |
| Lines read | 42 |
| Nonblank lines | 30 |
| SHA-256 prefix | da8fc1ec0fa54030 |
| First line | # Scope and Objectives |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 13 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-AGENT-003, FR-CODE-002, FR-CONN-002, FR-CONN-003, FR-RAG-004 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Scope and Objectives |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 28 | ## Engineering rules |
| 36 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/03-functional-requirements.md

| Property | Value |
| --- | --- |
| Lines read | 683 |
| Nonblank lines | 610 |
| SHA-256 prefix | 64cb376f0dbe2231 |
| First line | # Functional Requirements |
| Last line | **TARGET PHASE:** P1-MVP |
| Requirement-like lines | 176 |
| Status/gap/risk-like lines | 82 |
| Requirement IDs seen | FR-ADMIN-001, FR-ADMIN-002, FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, FR-CODE-001, FR-CODE-002, FR-CODE-003, FR-CODE-004, FR-CODE-005, FR-CONF-001, FR-CONN-001, FR-CONN-002, FR-CONN-003, FR-CONN-004, FR-CONN-005, FR-CONN-006, FR-CONN-007, FR-GRAPH-001, FR-GRAPH-002, FR-GRAPH-003, FR-GRAPH-004, FR-GRAPH-005, FR-GRAPH-006, FR-GRAPH-007, FR-GRAPH-008, FR-GRAPH-009, FR-GRAPH-010, FR-ID-001, FR-ID-002, FR-INGEST-001, FR-INGEST-002, FR-INGEST-003, FR-INGEST-004, FR-INGEST-005, FR-MCP-001, FR-MCP-002, FR-MEM-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Functional Requirements |
| 11 | ### FR-CONN-001 — Connector SDK |
| 21 | ### FR-CONN-002 — Jira JSON connector |
| 31 | ### FR-CONN-003 — Git repository connector |
| 41 | ### FR-CONN-004 — GitLab metadata adapter |
| 51 | ### FR-CONN-005 — Connector resiliency |
| 61 | ### FR-CONN-006 — Dry run and replay |
| 71 | ### FR-CONN-007 — Source deletion semantics |
| 81 | ### FR-CONF-001 — Confluence connector |
| 91 | ### FR-SNOW-001 — ServiceNow connector |
| 101 | ### FR-INGEST-001 — Raw capture |
| 111 | ### FR-INGEST-002 — Canonicalization |
| 121 | ### FR-INGEST-003 — Idempotent mutation |
| 131 | ### FR-INGEST-004 — Ingestion job lifecycle |
| 141 | ### FR-INGEST-005 — Dead-letter processing |
| 151 | ### FR-GRAPH-001 — HugeGraph authoritative store |
| 161 | ### FR-GRAPH-002 — Logical graph domains |
| 171 | ### FR-GRAPH-003 — Schema bootstrap |
| 181 | ### FR-GRAPH-004 — Canonical identifiers |
| 191 | ### FR-GRAPH-005 — Meta graph |
| 201 | ### FR-GRAPH-006 — Cross-domain bridge edges |
| 211 | ### FR-GRAPH-007 — Gremlin repository |
| 221 | ### FR-GRAPH-008 — Index strategy |
| 231 | ### FR-GRAPH-009 — Graph version journal |
| 241 | ### FR-GRAPH-010 — RDF/OWL interoperability |
| 255 | ### FR-ONTO-001 — Enterprise ontology vocabulary |
| 265 | ### FR-ONTO-002 — Relationship semantics |
| 275 | ### FR-PROV-001 — Evidence model |
| 285 | ### FR-PROV-002 — Provenance traversal |
| 295 | ### FR-ID-001 — Deterministic identity resolution |
| 305 | ### FR-ID-002 — Ambiguous identity candidates |
| 315 | ### FR-TEMP-001 — Bitemporal-ready fields |
| 325 | ### FR-CODE-001 — Deterministic code parser |
| 335 | ### FR-CODE-002 — Python and TypeScript MVP parsing |
| 345 | ### FR-CODE-003 — Commit-to-symbol linking |
| 355 | ### FR-CODE-004 — Call/import/dependency edges |
| 365 | ### FR-CODE-005 — Source navigation |
| 375 | ### FR-QUERY-001 — Structured QueryPlan |
| 385 | ### FR-QUERY-002 — Path query |
| 395 | ### FR-QUERY-003 — Impact analysis |
| 405 | ### FR-QUERY-004 — Entity search |
| 415 | ### FR-QUERY-005 — Natural-language query interpretation |
| 425 | ### FR-QUERY-006 — Query safety policy |
| 435 | ### FR-QUERY-007 — Query evidence envelope |
| 445 | ### FR-QUERY-008 — Raw Gremlin admin boundary |
| 455 | ### FR-VALID-001 — Graph validation rules |
| 465 | ### FR-VALID-002 — Validation gates |
| 475 | ### FR-VALID-003 — Graph quality metrics |
| 485 | ### FR-RAG-001 — Retrieval router |
| 495 | ### FR-RAG-002 — GraphRAG evidence retrieval |
| 505 | ### FR-RAG-003 — Local model abstraction |
| 515 | ### FR-RAG-004 — No mandatory vector DB in MVP |
| 525 | ### FR-RAG-005 — RAG evaluation harness |
| 535 | ### FR-RAG-006 — Adaptive RAG strategy framework |
| 545 | ### FR-AGENT-001 — Agent contract |
| 555 | ### FR-AGENT-002 — Bounded agent runtime |
| 565 | ### FR-AGENT-003 — TraceImpact agent |
| 575 | ### FR-AGENT-004 — Write/action approval boundary |
| 585 | ### FR-AGENT-005 — Controlled self-modification |
| 595 | ### FR-MEM-001 — Scoped memory records |
| 605 | ### FR-MCP-001 — MCP read server |
| 615 | ### FR-MCP-002 — MCP action separation |
| 625 | ### FR-UI-001 — User web application |
| 635 | ### FR-UI-002 — Graph explorer |
| 645 | ### FR-ADMIN-001 — Admin ingestion UI |
| 655 | ### FR-ADMIN-002 — Admin graph quality UI |
| 665 | ### FR-VSCODE-001 — VS Code context extension |
| 675 | ### FR-VSCODE-002 — VS Code trace/impact commands |

### EOIP-engg-doc-pkg/04-non-functional-requirements.md

| Property | Value |
| --- | --- |
| Lines read | 171 |
| Nonblank lines | 146 |
| SHA-256 prefix | 320a62c9ffdb4729 |
| First line | # Non-Functional Requirements |
| Last line | - Write/destructive MCP/agent tools are not registered in the MVP. |
| Requirement-like lines | 49 |
| Status/gap/risk-like lines | 17 |
| Requirement IDs seen | NFR-MAINT-001, NFR-OPS-001, NFR-OPS-002, NFR-PERF-001, NFR-PRIV-001, NFR-REL-001, NFR-REL-002, NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-005, NFR-SEC-006, NFR-SEC-007 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Non-Functional Requirements |
| 11 | ### NFR-SEC-001 — No outbound enterprise-data egress |
| 21 | ### NFR-SEC-002 — Secret isolation |
| 31 | ### NFR-SEC-003 — Input/file safety |
| 41 | ### NFR-SEC-004 — Prompt/tool injection defenses |
| 51 | ### NFR-SEC-005 — Authentication without MVP RBAC |
| 61 | ### NFR-SEC-006 — Container hardening |
| 71 | ### NFR-SEC-007 — Audit events |
| 81 | ### NFR-REL-001 — Restart-safe processing |
| 91 | ### NFR-REL-002 — Backup and restore |
| 101 | ### NFR-OPS-001 — Structured logging and health |
| 111 | ### NFR-OPS-002 — Local metrics |
| 121 | ### NFR-PERF-001 — Benchmark-defined objectives |
| 131 | ### NFR-MAINT-001 — Modular monolith boundary |
| 141 | ### NFR-PRIV-001 — Data minimization and classification |
| 153 | ## MVP benchmark definition (targets, not measured claims) |
| 161 | ## Phase 1 security baseline |

### EOIP-engg-doc-pkg/05-system-requirements.md

| Property | Value |
| --- | --- |
| Lines read | 42 |
| Nonblank lines | 30 |
| SHA-256 prefix | 4c873fc951d3b2b0 |
| First line | # System Requirements |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 10 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-GRAPH-001, NFR-OPS-001, NFR-REL-001, NFR-SEC-001, NFR-SEC-006 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # System Requirements |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 28 | ## Engineering rules |
| 36 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/06-architecture.md

| Property | Value |
| --- | --- |
| Lines read | 333 |
| Nonblank lines | 266 |
| SHA-256 prefix | 378ea79b522f93f1 |
| First line | # Target Architecture |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 98 |
| Status/gap/risk-like lines | 11 |
| Requirement IDs seen | FR-AGENT-002, FR-GRAPH-001, FR-GRAPH-002, FR-GRAPH-006, FR-GRAPH-011, FR-QUERY-001, FR-RAG-003, GAP-FABRIC-001..008, GAP-OPS-001, NFR-MAINT-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Target Architecture |
| 14 | ## Scope and Design Intent |
| 30 | ## Architecture Decisions |
| 45 | ## Architecture Diagrams |
| 89 | ## Implementation Reference |
| 93 | ### Docker Services |
| 106 | ### Application Packages (`packages/eoip/`) |
| 128 | ### Data Flows |
| 130 | #### 1. Source Ingestion Path |
| 154 | #### 2. Query Path |
| 173 | #### 3. RAG Path |
| 189 | #### 4. Agent Path |
| 203 | ### Graph Schema |
| 205 | #### Authoritative Domains (14) |
| 209 | #### Core Vertex Labels (40+) |
| 219 | #### Core Edge Labels (30+) |
| 225 | #### Index Strategy (12+ indexes) |
| 232 | ### Security Architecture |
| 244 | ### Observability |
| 254 | ### Storage |
| 268 | ### Multi-Backend GraphStore |
| 280 | ### Federated Query Planner (`packages/eoip/federation/planner.py`) |
| 292 | ### Deployment Reference |
| 300 | ## Applicable Requirements |
| 317 | ## Engineering Rules |
| 327 | ## Validation / Definition of Done |

### EOIP-engg-doc-pkg/07-component-architecture.md

| Property | Value |
| --- | --- |
| Lines read | 72 |
| Nonblank lines | 54 |
| SHA-256 prefix | d3a24cfb3b2ed58d |
| First line | # Component Architecture |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 30 |
| Status/gap/risk-like lines | 4 |
| Requirement IDs seen | FR-AGENT-001, FR-CONN-001, FR-GRAPH-007, FR-INGEST-002, FR-MCP-001, FR-RAG-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Component Architecture |
| 11 | ## Scope and design intent |
| 24 | ## Architecture decisions |
| 47 | ## Applicable requirements |
| 58 | ## Engineering rules |
| 66 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/08-deployment-architecture.md

| Property | Value |
| --- | --- |
| Lines read | 79 |
| Nonblank lines | 63 |
| SHA-256 prefix | 9d51ccb4232b1759 |
| First line | # Deployment Architecture |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 34 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen | FR-GRAPH-001, NFR-OPS-001, NFR-SEC-001, NFR-SEC-006 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Deployment Architecture |
| 11 | ## Scope and design intent |
| 20 | ## Architecture decisions |
| 56 | ## Applicable requirements |
| 65 | ## Engineering rules |
| 73 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/09-data-architecture.md

| Property | Value |
| --- | --- |
| Lines read | 44 |
| Nonblank lines | 31 |
| SHA-256 prefix | 61d1dcff86d4f1c9 |
| First line | # Data Architecture |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 14 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen | FR-GRAPH-004, FR-INGEST-001, FR-INGEST-002, FR-PROV-001, NFR-PRIV-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Data Architecture |
| 11 | ## Scope and design intent |
| 20 | ## Applicable requirements |
| 30 | ## Engineering rules |
| 38 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/10-enterprise-ontology.md

| Property | Value |
| --- | --- |
| Lines read | 40 |
| Nonblank lines | 28 |
| SHA-256 prefix | 575ab79dc9c8a8ce |
| First line | # Enterprise Ontology |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 12 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-GRAPH-010, FR-ONTO-001, FR-ONTO-002 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Enterprise Ontology |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 26 | ## Engineering rules |
| 34 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/11-graph-schema.md

| Property | Value |
| --- | --- |
| Lines read | 62 |
| Nonblank lines | 42 |
| SHA-256 prefix | fe22f215c4a66449 |
| First line | # HugeGraph Graph Schema |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 15 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen | FR-GRAPH-003, FR-GRAPH-004, FR-GRAPH-008, FR-ONTO-002 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # HugeGraph Graph Schema |
| 11 | ## Scope and design intent |
| 20 | ## MVP HugeGraph schema |
| 22 | ### Shared property keys |
| 25 | ### MVP vertex labels |
| 30 | ### MVP edge labels |
| 33 | ### Index baseline |
| 36 | ### Uniqueness and idempotency |
| 39 | ## Applicable requirements |
| 48 | ## Engineering rules |
| 56 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/12-meta-graph-design.md

| Property | Value |
| --- | --- |
| Lines read | 40 |
| Nonblank lines | 28 |
| SHA-256 prefix | 6341b6e7c1b9ba8a |
| First line | # Meta Graph Design |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 14 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-GRAPH-005, FR-INGEST-004, FR-VALID-003 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Meta Graph Design |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 26 | ## Engineering rules |
| 34 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/13-relationship-model.md

| Property | Value |
| --- | --- |
| Lines read | 40 |
| Nonblank lines | 28 |
| SHA-256 prefix | 1f05151a7643b0be |
| First line | # Relationship Model |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 9 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-GRAPH-006, FR-ONTO-002, FR-PROV-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Relationship Model |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 26 | ## Engineering rules |
| 34 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/14-temporal-graph.md

| Property | Value |
| --- | --- |
| Lines read | 39 |
| Nonblank lines | 27 |
| SHA-256 prefix | f01e0612210929d5 |
| First line | # Temporal Graph |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 11 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-GRAPH-009, FR-TEMP-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Temporal Graph |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 25 | ## Engineering rules |
| 33 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/15-provenance-lineage.md

| Property | Value |
| --- | --- |
| Lines read | 40 |
| Nonblank lines | 28 |
| SHA-256 prefix | dab70baf28956a5c |
| First line | # Provenance and Lineage |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 11 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-INGEST-001, FR-PROV-001, FR-PROV-002 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Provenance and Lineage |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 26 | ## Engineering rules |
| 34 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/16-identity-resolution.md

| Property | Value |
| --- | --- |
| Lines read | 39 |
| Nonblank lines | 27 |
| SHA-256 prefix | 830ae3dd340aa98b |
| First line | # Identity Resolution |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 8 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-ID-001, FR-ID-002 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Identity Resolution |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 25 | ## Engineering rules |
| 33 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/17-code-graph.md

| Property | Value |
| --- | --- |
| Lines read | 42 |
| Nonblank lines | 30 |
| SHA-256 prefix | d91b112a87f4ba9b |
| First line | # Code Graph |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 12 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-CODE-001, FR-CODE-002, FR-CODE-003, FR-CODE-004, FR-CODE-005 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Code Graph |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 28 | ## Engineering rules |
| 36 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/18-ingestion-architecture.md

| Property | Value |
| --- | --- |
| Lines read | 53 |
| Nonblank lines | 39 |
| SHA-256 prefix | 3e93ca3b2205284a |
| First line | # Ingestion Architecture |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 15 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-INGEST-001, FR-INGEST-002, FR-INGEST-003, FR-INGEST-004, FR-INGEST-005 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Ingestion Architecture |
| 11 | ## Scope and design intent |
| 29 | ## Applicable requirements |
| 39 | ## Engineering rules |
| 47 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/19-connector-framework.md

| Property | Value |
| --- | --- |
| Lines read | 41 |
| Nonblank lines | 29 |
| SHA-256 prefix | b1e1d92bc0f14632 |
| First line | # Connector Framework |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 13 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-CONN-001, FR-CONN-005, FR-CONN-006, FR-CONN-007 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Connector Framework |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 27 | ## Engineering rules |
| 35 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/20-jira-connector-requirements.md

| Property | Value |
| --- | --- |
| Lines read | 39 |
| Nonblank lines | 27 |
| SHA-256 prefix | 03ece9c052dffe27 |
| First line | # Jira Connector Requirements |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 12 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-CONN-002, FR-INGEST-002 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Jira Connector Requirements |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 25 | ## Engineering rules |
| 33 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/21-confluence-connector-requirements.md

| Property | Value |
| --- | --- |
| Lines read | 38 |
| Nonblank lines | 26 |
| SHA-256 prefix | 91eb356b39a6e57f |
| First line | # Confluence Connector Requirements |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 12 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-CONF-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Confluence Connector Requirements |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 24 | ## Engineering rules |
| 32 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/22-gitlab-connector-requirements.md

| Property | Value |
| --- | --- |
| Lines read | 40 |
| Nonblank lines | 28 |
| SHA-256 prefix | 97b43c085178485d |
| First line | # Git/GitLab Connector Requirements |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 12 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-CODE-003, FR-CONN-003, FR-CONN-004 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Git/GitLab Connector Requirements |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 26 | ## Engineering rules |
| 34 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/23-servicenow-connector-requirements.md

| Property | Value |
| --- | --- |
| Lines read | 38 |
| Nonblank lines | 26 |
| SHA-256 prefix | fad7d4bb88d6979b |
| First line | # ServiceNow Connector Requirements |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 12 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-SNOW-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # ServiceNow Connector Requirements |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 24 | ## Engineering rules |
| 32 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/24-file-web-connectors.md

| Property | Value |
| --- | --- |
| Lines read | 42 |
| Nonblank lines | 29 |
| SHA-256 prefix | eb3eba2f719d6c98 |
| First line | # File and Intranet Connector Requirements |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 15 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen | FR-CONN-001, NFR-PRIV-001, NFR-SEC-003 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # File and Intranet Connector Requirements |
| 11 | ## Scope and design intent |
| 20 | ## Applicable requirements |
| 28 | ## Engineering rules |
| 36 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/25-query-engine-requirements.md

| Property | Value |
| --- | --- |
| Lines read | 57 |
| Nonblank lines | 41 |
| SHA-256 prefix | d9d5bf16ceec79b4 |
| First line | # Query Engine Requirements |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 17 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-QUERY-001, FR-QUERY-002, FR-QUERY-003, FR-QUERY-004, FR-QUERY-005, FR-QUERY-006, FR-QUERY-007, FR-QUERY-008, FR-QUERY-009 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Query Engine Requirements |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 32 | ## Natural-language query processor |
| 43 | ## Engineering rules |
| 51 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/26-query-engine-implementation.md

| Property | Value |
| --- | --- |
| Lines read | 66 |
| Nonblank lines | 51 |
| SHA-256 prefix | 3a1c64f75138a2db |
| First line | # Query Engine Implementation |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 15 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-GRAPH-007, FR-QUERY-001, FR-QUERY-002, FR-QUERY-003 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Query Engine Implementation |
| 11 | ## Scope and design intent |
| 32 | ## NLQ processor design |
| 43 | ## Applicable requirements |
| 52 | ## Engineering rules |
| 60 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/27-ontology-validation.md

| Property | Value |
| --- | --- |
| Lines read | 39 |
| Nonblank lines | 27 |
| SHA-256 prefix | 60d4bf8611772fde |
| First line | # Ontology Validation |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 13 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-VALID-001, FR-VALID-002 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Ontology Validation |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 25 | ## Engineering rules |
| 33 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/28-graph-quality.md

| Property | Value |
| --- | --- |
| Lines read | 39 |
| Nonblank lines | 27 |
| SHA-256 prefix | fca6db75053af9c4 |
| First line | # Graph Quality |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 11 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-PROV-001, FR-VALID-003 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Graph Quality |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 25 | ## Engineering rules |
| 33 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/29-rag-architecture.md

| Property | Value |
| --- | --- |
| Lines read | 58 |
| Nonblank lines | 44 |
| SHA-256 prefix | 5e54064da716a275 |
| First line | # RAG Architecture |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 19 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-RAG-001, FR-RAG-002, FR-RAG-003, FR-RAG-004, FR-RAG-005, FR-RAG-006 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # RAG Architecture |
| 11 | ## Scope and design intent |
| 33 | ## Applicable requirements |
| 44 | ## Engineering rules |
| 52 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/30-agent-architecture.md

| Property | Value |
| --- | --- |
| Lines read | 61 |
| Nonblank lines | 47 |
| SHA-256 prefix | c3ed1557a759f09a |
| First line | # Agent Architecture |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 21 |
| Status/gap/risk-like lines | 4 |
| Requirement IDs seen | FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Agent Architecture |
| 11 | ## Scope and design intent |
| 37 | ## Applicable requirements |
| 47 | ## Engineering rules |
| 55 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/31-multi-agent-architecture.md

| Property | Value |
| --- | --- |
| Lines read | 40 |
| Nonblank lines | 28 |
| SHA-256 prefix | eef840078cfd3b73 |
| First line | # Multi-Agent Architecture |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 13 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen | FR-AGENT-001, FR-AGENT-002, FR-AGENT-004 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Multi-Agent Architecture |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 26 | ## Engineering rules |
| 34 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/32-memory-engineering.md

| Property | Value |
| --- | --- |
| Lines read | 39 |
| Nonblank lines | 27 |
| SHA-256 prefix | 88ecb00f48144b36 |
| First line | # Memory Engineering |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 11 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen | FR-MEM-001, NFR-PRIV-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Memory Engineering |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 25 | ## Engineering rules |
| 33 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/33-context-engineering.md

| Property | Value |
| --- | --- |
| Lines read | 42 |
| Nonblank lines | 29 |
| SHA-256 prefix | c84989bb7e3d445e |
| First line | # Context Engineering |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 12 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-PROV-001, FR-QUERY-007, FR-RAG-002 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Context Engineering |
| 11 | ## Scope and design intent |
| 20 | ## Applicable requirements |
| 28 | ## Engineering rules |
| 36 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/34-loop-engineering.md

| Property | Value |
| --- | --- |
| Lines read | 38 |
| Nonblank lines | 26 |
| SHA-256 prefix | 99365da1f8722607 |
| First line | # Loop Engineering |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 10 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen | FR-AGENT-002 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Loop Engineering |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 24 | ## Engineering rules |
| 32 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/35-graph-engineering.md

| Property | Value |
| --- | --- |
| Lines read | 42 |
| Nonblank lines | 29 |
| SHA-256 prefix | 32bd915a1f0ecda5 |
| First line | # Graph Engineering |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 15 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen | FR-GRAPH-002, FR-GRAPH-006, FR-GRAPH-008 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Graph Engineering |
| 11 | ## Scope and design intent |
| 20 | ## Applicable requirements |
| 28 | ## Engineering rules |
| 36 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/36-harness-engineering.md

| Property | Value |
| --- | --- |
| Lines read | 42 |
| Nonblank lines | 29 |
| SHA-256 prefix | 96bab7392e47c670 |
| First line | # Harness Engineering |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 12 |
| Status/gap/risk-like lines | 4 |
| Requirement IDs seen | FR-AGENT-001, FR-AGENT-002, NFR-OPS-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Harness Engineering |
| 11 | ## Scope and design intent |
| 20 | ## Applicable requirements |
| 28 | ## Engineering rules |
| 36 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/37-graph-over-loop.md

| Property | Value |
| --- | --- |
| Lines read | 41 |
| Nonblank lines | 28 |
| SHA-256 prefix | d24e82f0ba204915 |
| First line | # Graph-over-Loop Engineering |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 14 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen | FR-AGENT-002, FR-GRAPH-005 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Graph-over-Loop Engineering |
| 11 | ## Scope and design intent |
| 20 | ## Applicable requirements |
| 27 | ## Engineering rules |
| 35 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/38-loop-over-graph.md

| Property | Value |
| --- | --- |
| Lines read | 40 |
| Nonblank lines | 28 |
| SHA-256 prefix | 485afc1c22f72037 |
| First line | # Loop-over-Graph Engineering |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 12 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-AGENT-002, FR-QUERY-003, FR-QUERY-006 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Loop-over-Graph Engineering |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 26 | ## Engineering rules |
| 34 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/39-mcp-architecture.md

| Property | Value |
| --- | --- |
| Lines read | 40 |
| Nonblank lines | 28 |
| SHA-256 prefix | 8b6b87c21af8527f |
| First line | # MCP Architecture |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 13 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-AGENT-004, FR-MCP-001, FR-MCP-002 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # MCP Architecture |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 26 | ## Engineering rules |
| 34 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/40-human-control-model.md

| Property | Value |
| --- | --- |
| Lines read | 39 |
| Nonblank lines | 27 |
| SHA-256 prefix | bded93a051cefc64 |
| First line | # Human Control Model |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 10 |
| Status/gap/risk-like lines | 4 |
| Requirement IDs seen | FR-AGENT-004, FR-AGENT-005 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Human Control Model |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 25 | ## Engineering rules |
| 33 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/41-xai-explainability.md

| Property | Value |
| --- | --- |
| Lines read | 40 |
| Nonblank lines | 28 |
| SHA-256 prefix | 6ca04e7069563b68 |
| First line | # XAI and Explainability |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 11 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-PROV-001, FR-QUERY-007, FR-RAG-002 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # XAI and Explainability |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 26 | ## Engineering rules |
| 34 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/42-web-user-ui-ux.md

| Property | Value |
| --- | --- |
| Lines read | 40 |
| Nonblank lines | 28 |
| SHA-256 prefix | e132992f6e40fc08 |
| First line | # Web User UI/UX |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 12 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-QUERY-004, FR-UI-001, FR-UI-002 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Web User UI/UX |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 26 | ## Engineering rules |
| 34 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/43-admin-ui-ux.md

| Property | Value |
| --- | --- |
| Lines read | 43 |
| Nonblank lines | 30 |
| SHA-256 prefix | 51418136f2da9db1 |
| First line | # Admin UI/UX |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 16 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-ADMIN-001, FR-ADMIN-002, FR-INGEST-004, FR-VALID-003 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Admin UI/UX |
| 11 | ## Scope and design intent |
| 20 | ## Applicable requirements |
| 29 | ## Engineering rules |
| 37 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/44-vscode-extension.md

| Property | Value |
| --- | --- |
| Lines read | 42 |
| Nonblank lines | 29 |
| SHA-256 prefix | 2fa124c6b2cbdf3d |
| First line | # VS Code Extension |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 12 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-CODE-005, FR-VSCODE-001, FR-VSCODE-002 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # VS Code Extension |
| 11 | ## Scope and design intent |
| 20 | ## Applicable requirements |
| 28 | ## Engineering rules |
| 36 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/45-api-specification.md

| Property | Value |
| --- | --- |
| Lines read | 43 |
| Nonblank lines | 30 |
| SHA-256 prefix | 0490c01bc97d2f6a |
| First line | # API Specification |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 14 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-AGENT-003, FR-INGEST-004, FR-QUERY-001, FR-QUERY-007 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # API Specification |
| 11 | ## Scope and design intent |
| 20 | ## Applicable requirements |
| 29 | ## Engineering rules |
| 37 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/46-security-architecture.md

| Property | Value |
| --- | --- |
| Lines read | 56 |
| Nonblank lines | 42 |
| SHA-256 prefix | ad4920a094b72336 |
| First line | # Security Architecture |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 19 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen | NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-005, NFR-SEC-006, NFR-SEC-007 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Security Architecture |
| 11 | ## Scope and design intent |
| 18 | ## Phase 1 security baseline |
| 30 | ## Applicable requirements |
| 42 | ## Engineering rules |
| 50 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/47-threat-model.md

| Property | Value |
| --- | --- |
| Lines read | 49 |
| Nonblank lines | 39 |
| SHA-256 prefix | 99300cd99900462c |
| First line | # Threat Model |
| Last line | - Write/destructive MCP/agent tools are not registered in the MVP. |
| Requirement-like lines | 20 |
| Status/gap/risk-like lines | 4 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Threat Model |
| 11 | ## Trust boundaries and assets |
| 15 | ## Threat register |
| 35 | ## Residual-risk rule |
| 39 | ## Phase 1 security baseline |

### EOIP-engg-doc-pkg/48-data-privacy.md

| Property | Value |
| --- | --- |
| Lines read | 40 |
| Nonblank lines | 28 |
| SHA-256 prefix | 0552010a6a511631 |
| First line | # Data Privacy |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 12 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen | NFR-PRIV-001, NFR-SEC-002, NFR-SEC-007 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Data Privacy |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 26 | ## Engineering rules |
| 34 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/49-local-ai-model-strategy.md

| Property | Value |
| --- | --- |
| Lines read | 40 |
| Nonblank lines | 28 |
| SHA-256 prefix | de1cb70f9ff2fbd6 |
| First line | # Local AI Model Strategy |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 11 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-RAG-003, FR-RAG-004, NFR-SEC-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Local AI Model Strategy |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 26 | ## Engineering rules |
| 34 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/50-observability.md

| Property | Value |
| --- | --- |
| Lines read | 38 |
| Nonblank lines | 27 |
| SHA-256 prefix | 6970b55ea4e5c583 |
| First line | # Observability |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 10 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | NFR-OPS-001, NFR-OPS-002, NFR-SEC-007 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Observability |
| 11 | ## Scope and design intent |
| 16 | ## Applicable requirements |
| 24 | ## Engineering rules |
| 32 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/51-performance.md

| Property | Value |
| --- | --- |
| Lines read | 45 |
| Nonblank lines | 30 |
| SHA-256 prefix | 5f805a1ef26d4601 |
| First line | # Performance Engineering |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 13 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen | FR-GRAPH-008, NFR-PERF-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Performance Engineering |
| 11 | ## Scope and design intent |
| 18 | ## MVP benchmark definition (targets, not measured claims) |
| 24 | ## Applicable requirements |
| 31 | ## Engineering rules |
| 39 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/52-scalability.md

| Property | Value |
| --- | --- |
| Lines read | 40 |
| Nonblank lines | 28 |
| SHA-256 prefix | 78f1f8edf18cec3d |
| First line | # Scalability |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 10 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-GRAPH-002, NFR-MAINT-001, NFR-PERF-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Scalability |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 26 | ## Engineering rules |
| 34 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/53-backup-restore.md

| Property | Value |
| --- | --- |
| Lines read | 38 |
| Nonblank lines | 26 |
| SHA-256 prefix | 8f0c89d7fdae0847 |
| First line | # Backup and Restore |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 12 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | NFR-REL-002 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Backup and Restore |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 24 | ## Engineering rules |
| 32 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/54-devsecops.md

| Property | Value |
| --- | --- |
| Lines read | 40 |
| Nonblank lines | 28 |
| SHA-256 prefix | 0b2828d21715beb0 |
| First line | # DevSecOps |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 8 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen | NFR-MAINT-001, NFR-SEC-002, NFR-SEC-006 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # DevSecOps |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 26 | ## Engineering rules |
| 34 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/55-testing-strategy.md

| Property | Value |
| --- | --- |
| Lines read | 110 |
| Nonblank lines | 103 |
| SHA-256 prefix | 8144dd3192640122 |
| First line | # Testing Strategy |
| Last line | - **NFR-PRIV-001** — Redaction fixtures. Completion signal: Audit/log exports contain no prohibited content. |
| Requirement-like lines | 58 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-ADMIN-001, FR-ADMIN-002, FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, FR-CODE-001, FR-CODE-002, FR-CODE-003, FR-CODE-004, FR-CODE-005, FR-CONF-001, FR-CONN-001, FR-CONN-002, FR-CONN-003, FR-CONN-004, FR-CONN-005, FR-CONN-006, FR-CONN-007, FR-GRAPH-001, FR-GRAPH-002, FR-GRAPH-003, FR-GRAPH-004, FR-GRAPH-005, FR-GRAPH-006, FR-GRAPH-007, FR-GRAPH-008, FR-GRAPH-009, FR-GRAPH-010, FR-ID-001, FR-ID-002, FR-INGEST-001, FR-INGEST-002, FR-INGEST-003, FR-INGEST-004, FR-INGEST-005, FR-MCP-001, FR-MCP-002, FR-MEM-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Testing Strategy |
| 13 | ## Test layers |
| 28 | ## Requirement-to-test obligations |

### EOIP-engg-doc-pkg/56-rag-agent-evaluation.md

| Property | Value |
| --- | --- |
| Lines read | 42 |
| Nonblank lines | 29 |
| SHA-256 prefix | c1c60235456e071c |
| First line | # RAG and Agent Evaluation |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 14 |
| Status/gap/risk-like lines | 4 |
| Requirement IDs seen | FR-AGENT-002, FR-AGENT-003, FR-RAG-005 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # RAG and Agent Evaluation |
| 11 | ## Scope and design intent |
| 20 | ## Applicable requirements |
| 28 | ## Engineering rules |
| 36 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/57-graph-validation-test-plan.md

| Property | Value |
| --- | --- |
| Lines read | 43 |
| Nonblank lines | 30 |
| SHA-256 prefix | 56db120b4aa616ee |
| First line | # Graph Validation Test Plan |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 15 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen | FR-PROV-001, FR-VALID-001, FR-VALID-002, FR-VALID-003 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Graph Validation Test Plan |
| 11 | ## Scope and design intent |
| 20 | ## Applicable requirements |
| 29 | ## Engineering rules |
| 37 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/58-end-to-end-test-plan.md

| Property | Value |
| --- | --- |
| Lines read | 42 |
| Nonblank lines | 30 |
| SHA-256 prefix | b9455a372b8783b3 |
| First line | # End-to-End Test Plan |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 14 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen | FR-AGENT-003, FR-GRAPH-006, FR-MCP-001, FR-VSCODE-001, NFR-REL-002 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # End-to-End Test Plan |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 28 | ## Engineering rules |
| 36 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/59-docker-deployment.md

| Property | Value |
| --- | --- |
| Lines read | 64 |
| Nonblank lines | 51 |
| SHA-256 prefix | eb03176662a12d24 |
| First line | # Docker Deployment |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 26 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-GRAPH-001, NFR-OPS-001, NFR-SEC-001, NFR-SEC-006 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Docker Deployment |
| 11 | ## Scope and design intent |
| 41 | ## Applicable requirements |
| 50 | ## Engineering rules |
| 58 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/60-operational-runbook.md

| Property | Value |
| --- | --- |
| Lines read | 41 |
| Nonblank lines | 29 |
| SHA-256 prefix | ef9949f7fbdf855c |
| First line | # Operational Runbook |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 10 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | NFR-OPS-001, NFR-OPS-002, NFR-REL-001, NFR-REL-002 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Operational Runbook |
| 11 | ## Scope and design intent |
| 18 | ## Applicable requirements |
| 27 | ## Engineering rules |
| 35 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/61-demo-playbook.md

| Property | Value |
| --- | --- |
| Lines read | 61 |
| Nonblank lines | 46 |
| SHA-256 prefix | ebaeaf581099c518 |
| First line | # Demo Playbook |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 15 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-GRAPH-006, FR-MCP-001, FR-QUERY-002, FR-QUERY-003, FR-RAG-002, FR-VSCODE-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Demo Playbook |
| 11 | ## Scope and design intent |
| 36 | ## Applicable requirements |
| 47 | ## Engineering rules |
| 55 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/62-risk-register.md

| Property | Value |
| --- | --- |
| Lines read | 27 |
| Nonblank lines | 24 |
| SHA-256 prefix | 03d8a989d2d5c6a0 |
| First line | # Risk Register |
| Last line | \| R-015 \| Self-improving capability bypasses governance \| L before P8 \| Critical \| no implementation path before governance/sandbox/approval/regression/rollback \| P8+ \| |
| Requirement-like lines | 11 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Risk Register |

### EOIP-engg-doc-pkg/63-assumptions.md

| Property | Value |
| --- | --- |
| Lines read | 31 |
| Nonblank lines | 23 |
| SHA-256 prefix | 7aa01411ac203d6c |
| First line | # Assumptions |
| Last line | Each assumption becomes an ADR/update when actual enterprise samples, capacity targets, authentication/SSO requirements, network topology, language mix or recovery objectives are supplied. None should be silently converted into a product claim. |
| Requirement-like lines | 12 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Assumptions |
| 11 | ## Confirmed from the governing specification |
| 19 | ## Working assumptions introduced by this baseline |
| 29 | ## Validation triggers |

### EOIP-engg-doc-pkg/64-decisions-and-adrs.md

| Property | Value |
| --- | --- |
| Lines read | 39 |
| Nonblank lines | 27 |
| SHA-256 prefix | 56297c0d7fa2ad13 |
| First line | # Architecture Decisions and ADRs |
| Last line | **Status:** Accepted. **Decision:** clients never depend on HugeGraph internal IDs; storage topology/schema implementation can evolve behind stable contracts. |
| Requirement-like lines | 11 |
| Status/gap/risk-like lines | 1 |
| Requirement IDs seen | ADR-001, ADR-002, ADR-003, ADR-004, ADR-005, ADR-006, ADR-007, ADR-008, ADR-009, ADR-010 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Architecture Decisions and ADRs |
| 11 | ## ADR-001 — Logical domains in one physical HugeGraph graph for MVP |
| 14 | ## ADR-002 — RocksDB standalone HugeGraph for MVP |
| 17 | ## ADR-003 — Modular monolith application core |
| 20 | ## ADR-004 — Raw capture on local filesystem, HugeGraph as authoritative graph |
| 23 | ## ADR-005 — No mandatory vector database in P1 |
| 26 | ## ADR-006 — QueryPlan compilation, no unrestricted NL→Gremlin |
| 29 | ## ADR-007 — Read-only MCP/agent MVP |
| 32 | ## ADR-008 — Deterministic code and cross-domain linking first |
| 35 | ## ADR-009 — Local model abstraction and model-down degradation |
| 38 | ## ADR-010 — Versioned external contracts and canonical IDs |

### EOIP-engg-doc-pkg/65-glossary.md

| Property | Value |
| --- | --- |
| Lines read | 50 |
| Nonblank lines | 42 |
| SHA-256 prefix | adb5755791eb1298 |
| First line | # Glossary |
| Last line | Every policy is implemented using explicit dimensions: initiator, approver, supervisor, intervention trigger, action risk, reversibility, timeout behavior, exception path and evidence requirement. |
| Requirement-like lines | 15 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Glossary |
| 11 | ## Core terms |
| 29 | ## Human-control policy vocabulary |

### EOIP-engg-doc-pkg/66-phase-roadmap.md

| Property | Value |
| --- | --- |
| Lines read | 64 |
| Nonblank lines | 42 |
| SHA-256 prefix | 0abe43097d378431 |
| First line | # Phased Roadmap |
| Last line | \| FR-AGENT-005 — Controlled self-modification \| P8+ \| Stable canonical contracts, connector/query/agent ports and additive schema/versioning established in P1. \| |
| Requirement-like lines | 19 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen | FR-AGENT-005, FR-CONF-001, FR-GRAPH-010, FR-RAG-006, FR-SNOW-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Phased Roadmap |
| 11 | ## PHASE 0 — Architecture, schemas, development foundation |
| 16 | ## PHASE 1 — Fully functional demonstrable MVP |
| 21 | ## PHASE 2 — Enterprise connectors and ontology depth |
| 26 | ## PHASE 3 — Advanced GraphRAG and retrieval routing |
| 31 | ## PHASE 4 — Advanced agents and multi-agent workflows |
| 36 | ## PHASE 5 — Temporal intelligence and graph analytics |
| 41 | ## PHASE 6 — Human-control policies and automation |
| 46 | ## PHASE 7 — Enterprise hardening, scaling and operational maturity |
| 51 | ## PHASE 8+ — Advanced/self-improving capabilities |
| 56 | ## Deferred-requirement mapping |

### EOIP-engg-doc-pkg/67-implementation-plan.md

| Property | Value |
| --- | --- |
| Lines read | 265 |
| Nonblank lines | 230 |
| SHA-256 prefix | a1f98fb4bf0f5b95 |
| First line | # Master Implementation Plan |
| Last line | Every engineering ticket derived from this plan must contain: objective; mapped requirement IDs; dependencies; modules/files; versioned interfaces; ordered implementation steps; unit/contract/integration/security tests; acceptance evidence; expected artifacts; rollback/failure handling; observability; and documentation impact. |
| Requirement-like lines | 119 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen | FR-ADMIN-001, FR-ADMIN-002, FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, FR-CODE-001, FR-CODE-002, FR-CODE-003, FR-CODE-004, FR-CODE-005, FR-CONF-001, FR-CONN-001, FR-CONN-002, FR-CONN-003, FR-CONN-004, FR-CONN-005, FR-CONN-006, FR-CONN-007, FR-GRAPH-001, FR-GRAPH-002, FR-GRAPH-003, FR-GRAPH-004, FR-GRAPH-005, FR-GRAPH-006, FR-GRAPH-007, FR-GRAPH-008, FR-GRAPH-009, FR-GRAPH-010, FR-ID-001, FR-ID-002, FR-INGEST-001, FR-INGEST-002, FR-INGEST-003, FR-INGEST-004, FR-INGEST-005, FR-MCP-001, FR-MCP-002, FR-MEM-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Master Implementation Plan |
| 11 | ## Architecture decisions |
| 71 | ## Work packages |
| 73 | ### WP-FOUNDATION |
| 86 | ### WP-CONNECTORS |
| 103 | ### WP-INGESTION |
| 116 | ### WP-ONTOLOGY-GRAPH |
| 136 | ### WP-CODEGRAPH |
| 149 | ### WP-QUERY |
| 166 | ### WP-VALIDATION |
| 177 | ### WP-RAG |
| 191 | ### WP-AGENT-MEMORY |
| 205 | ### WP-MCP |
| 215 | ### WP-EXPERIENCE |
| 229 | ### WP-SECURITY-OPS |
| 252 | ## Sequencing rules |
| 263 | ## Requirement implementation template |

### EOIP-engg-doc-pkg/68-project-structure.md

| Property | Value |
| --- | --- |
| Lines read | 87 |
| Nonblank lines | 74 |
| SHA-256 prefix | 65a6a5522f63778f |
| First line | # Project Structure |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 27 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen | FR-CONN-001, FR-QUERY-001, NFR-MAINT-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Project Structure |
| 11 | ## Scope and design intent |
| 65 | ## Applicable requirements |
| 73 | ## Engineering rules |
| 81 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/69-dependency-license-sbom.md

| Property | Value |
| --- | --- |
| Lines read | 37 |
| Nonblank lines | 26 |
| SHA-256 prefix | 786168e188b0f10a |
| First line | # Dependency, License and SBOM |
| Last line | - Deferred capabilities remain behind stable interfaces and are not represented as already implemented. |
| Requirement-like lines | 7 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen | NFR-MAINT-001, NFR-SEC-006 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Dependency, License and SBOM |
| 11 | ## Scope and design intent |
| 16 | ## Applicable requirements |
| 23 | ## Engineering rules |
| 31 | ## Validation / definition of done |

### EOIP-engg-doc-pkg/70-acceptance-criteria.md

| Property | Value |
| --- | --- |
| Lines read | 131 |
| Nonblank lines | 122 |
| SHA-256 prefix | 0e81f7132284033c |
| First line | # Acceptance Criteria |
| Last line | A release candidate must include immutable build/version metadata, dependency/SBOM/license output, automated test report, schema/ontology version, known-risk register, clean-deployment evidence, no-egress test, demo evidence and verified backup/restore evidence. Any waived criterion requires an ADR/risk acceptance entry; MVP non-negotiables cannot be waived by implementation convenience. |
| Requirement-like lines | 77 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020, FR-021, FR-022, FR-023, FR-024, FR-025, FR-026, FR-027, FR-028, FR-ADMIN-001, FR-ADMIN-002, FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, FR-CODE-001, FR-CODE-002, FR-CODE-003, FR-CODE-004, FR-CODE-005 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Acceptance Criteria |
| 11 | ## Requirement acceptance criteria |
| 97 | ## MVP acceptance criteria |
| 129 | ## Release acceptance gate |

### EOIP-engg-doc-pkg/71-research-and-verification-basis.md

| Property | Value |
| --- | --- |
| Lines read | 31 |
| Nonblank lines | 23 |
| SHA-256 prefix | 566fe15c918c8ef0 |
| First line | # Research and Verification Basis |
| Last line | - Performance/scale numbers in this package are engineering targets or benchmark definitions unless explicitly marked as measured results. |
| Requirement-like lines | 9 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Research and Verification Basis |
| 11 | ## Verification principle |
| 15 | ## Primary references checked on 2026-10-01 |
| 26 | ## Claims deliberately not made |

### EOIP-engg-doc-pkg/72-requirement-traceability.md

| Property | Value |
| --- | --- |
| Lines read | 128 |
| Nonblank lines | 122 |
| SHA-256 prefix | 0befd674dec4ccad |
| First line | # Requirement Traceability Matrix |
| Last line | \| MVP-FR-028 — End-to-end demo \| FR-GRAPH-006,FR-AGENT-003 \| T28 \| |
| Requirement-like lines | 90 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen | AC-FR-ADMIN-001, AC-FR-ADMIN-002, AC-FR-AGENT-001, AC-FR-AGENT-002, AC-FR-AGENT-003, AC-FR-AGENT-004, AC-FR-AGENT-005, AC-FR-CODE-001, AC-FR-CODE-002, AC-FR-CODE-003, AC-FR-CODE-004, AC-FR-CODE-005, AC-FR-CONF-001, AC-FR-CONN-001, AC-FR-CONN-002, AC-FR-CONN-003, AC-FR-CONN-004, AC-FR-CONN-005, AC-FR-CONN-006, AC-FR-CONN-007, AC-FR-GRAPH-001, AC-FR-GRAPH-002, AC-FR-GRAPH-003, AC-FR-GRAPH-004, AC-FR-GRAPH-005, AC-FR-GRAPH-006, AC-FR-GRAPH-007, AC-FR-GRAPH-008, AC-FR-GRAPH-009, AC-FR-GRAPH-010, AC-FR-ID-001, AC-FR-ID-002, AC-FR-INGEST-001, AC-FR-INGEST-002, AC-FR-INGEST-003, AC-FR-INGEST-004, AC-FR-INGEST-005, AC-FR-MCP-001, AC-FR-MCP-002, AC-FR-MEM-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Requirement Traceability Matrix |
| 97 | ## MVP traceability |

### EOIP-engg-doc-pkg/73-architecture-diagrams.md

| Property | Value |
| --- | --- |
| Lines read | 293 |
| Nonblank lines | 257 |
| SHA-256 prefix | 093459aac532aaca |
| First line | # Architecture Diagram Catalog |
| Last line | ``` |
| Requirement-like lines | 77 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Architecture Diagram Catalog |
| 11 | ## 01-system-context |
| 30 | ## 02-container-architecture |
| 55 | ## 03-ingestion-pipeline |
| 66 | ## 04-enterprise-graph-architecture |
| 84 | ## 05-meta-graph |
| 99 | ## 06-code-graph |
| 112 | ## 07-cross-domain-relationship-graph |
| 128 | ## 08-query-execution |
| 143 | ## 09-graphrag |
| 158 | ## 10-agent-runtime |
| 177 | ## 11-multi-agent-orchestration |
| 195 | ## 12-mcp-architecture |
| 208 | ## 13-human-control-architecture |
| 222 | ## 14-web-ui-architecture |
| 237 | ## 15-vscode-architecture |
| 250 | ## 16-deployment |
| 272 | ## 17-mvp-e2e-flow |

### EOIP-engg-doc-pkg/74-data-contracts.md

| Property | Value |
| --- | --- |
| Lines read | 209 |
| Nonblank lines | 163 |
| SHA-256 prefix | c15dbe1425373dbc |
| First line | # Data Contracts |
| Last line | ``` |
| Requirement-like lines | 2 |
| Status/gap/risk-like lines | 1 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Data Contracts |
| 11 | ## Contract rules |
| 15 | ## SourceEvent v1 |
| 31 | ## NormalizedEntity v1 |
| 46 | ## NormalizedRelationship v1 |
| 62 | ## GraphMutation v1 |
| 76 | ## QueryPlan v1 |
| 90 | ## GraphResult v1 |
| 104 | ## RetrievalResult v1 |
| 117 | ## Evidence v1 |
| 131 | ## AgentRequest v1 |
| 143 | ## AgentResult v1 |
| 156 | ## ToolRequest v1 |
| 168 | ## ToolResult v1 |
| 179 | ## MemoryRecord v1 |
| 196 | ## AuditEvent v1 |

### EOIP-engg-doc-pkg/75-self-review-and-gap-closure.md

| Property | Value |
| --- | --- |
| Lines read | 40 |
| Nonblank lines | 26 |
| SHA-256 prefix | fef0185d9760b222 |
| First line | # Architecture Self-Review and Gap Closure |
| Last line | The documentation is considered architecture-baseline complete when the generated traceability catalog has no orphan requirement, every P1 mandatory item maps to one of T01–T28, and implementation teams revalidate pinned dependency versions before build. “Complete documentation” does not mean “implemented software”; the package is a build specification and execution plan. |
| Requirement-like lines | 12 |
| Status/gap/risk-like lines | 4 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Architecture Self-Review and Gap Closure |
| 11 | ## Review outcome |
| 13 | ### Enterprise / solution architecture |
| 16 | ### Graph / ontology architecture |
| 19 | ### AI / RAG architecture |
| 22 | ### Security architecture |
| 25 | ### Senior developer review |
| 28 | ### QA / reliability review |
| 31 | ### DevOps review |
| 34 | ## Remaining known unknowns |
| 38 | ## Completion statement |

### EOIP-engg-doc-pkg/76-multi-backend.md

| Property | Value |
| --- | --- |
| Lines read | 179 |
| Nonblank lines | 126 |
| SHA-256 prefix | e81496b6a52ee043 |
| First line | # EOIP Multi-Backend GraphStore |
| Last line | `tests/unit/test_graph_backends.py` covers backend registry, config loading, Neptune and Neo4j adapter contracts, env var overrides, and memory backend correctness. |
| Requirement-like lines | 25 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Multi-Backend GraphStore |
| 7 | ## Backend Registry (`packages/eoip/graph/backends.py`) |
| 25 | ## Supported Backends |
| 36 | ## Configuration (`config/graph-store.yaml`) |
| 39 | # Primary backend — which backend create_graph_store() returns |
| 71 | ### Environment Variable Overrides |
| 85 | ## Amazon Neptune Adapter (`packages/eoip/graph/neptune.py`) |
| 89 | ### Key design points |
| 97 | ### Neptune Endpoint Requirements |
| 108 | ## Neo4j Adapter (`packages/eoip/graph/neo4j.py`) |
| 112 | ### Key design points |
| 122 | ## GraphBackendCapabilities |
| 150 | ## Backend-Invariant Contract (`packages/eoip/graph/store.py`) |
| 169 | ## Supported Export Formats (All Backends) |
| 177 | ## Tests |

### EOIP-engg-doc-pkg/diagrams/01-system-context.md

| Property | Value |
| --- | --- |
| Lines read | 18 |
| Nonblank lines | 17 |
| SHA-256 prefix | 6f847a1ba8b1d0aa |
| First line | # 01-system-context |
| Last line | ``` |
| Requirement-like lines | 11 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # 01-system-context |

### EOIP-engg-doc-pkg/diagrams/02-container-architecture.md

| Property | Value |
| --- | --- |
| Lines read | 24 |
| Nonblank lines | 23 |
| SHA-256 prefix | c31b925367eaf0ef |
| First line | # 02-container-architecture |
| Last line | ``` |
| Requirement-like lines | 14 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # 02-container-architecture |

### EOIP-engg-doc-pkg/diagrams/03-ingestion-pipeline.md

| Property | Value |
| --- | --- |
| Lines read | 10 |
| Nonblank lines | 9 |
| SHA-256 prefix | f5f4117822eb038b |
| First line | # 03-ingestion-pipeline |
| Last line | ``` |
| Requirement-like lines | 3 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # 03-ingestion-pipeline |

### EOIP-engg-doc-pkg/diagrams/04-enterprise-graph-architecture.md

| Property | Value |
| --- | --- |
| Lines read | 17 |
| Nonblank lines | 16 |
| SHA-256 prefix | 2d71f91e5ff70a90 |
| First line | # 04-enterprise-graph-architecture |
| Last line | ``` |
| Requirement-like lines | 3 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # 04-enterprise-graph-architecture |

### EOIP-engg-doc-pkg/diagrams/05-meta-graph.md

| Property | Value |
| --- | --- |
| Lines read | 14 |
| Nonblank lines | 13 |
| SHA-256 prefix | 909fc44ec2001519 |
| First line | # 05-meta-graph |
| Last line | ``` |
| Requirement-like lines | 2 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # 05-meta-graph |

### EOIP-engg-doc-pkg/diagrams/06-code-graph.md

| Property | Value |
| --- | --- |
| Lines read | 12 |
| Nonblank lines | 11 |
| SHA-256 prefix | d6034dd75433ab01 |
| First line | # 06-code-graph |
| Last line | ``` |
| Requirement-like lines | 2 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # 06-code-graph |

### EOIP-engg-doc-pkg/diagrams/07-cross-domain-relationship-graph.md

| Property | Value |
| --- | --- |
| Lines read | 15 |
| Nonblank lines | 14 |
| SHA-256 prefix | 5cdc57d4e6d4a79f |
| First line | # 07-cross-domain-relationship-graph |
| Last line | ``` |
| Requirement-like lines | 1 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # 07-cross-domain-relationship-graph |

### EOIP-engg-doc-pkg/diagrams/08-query-execution.md

| Property | Value |
| --- | --- |
| Lines read | 14 |
| Nonblank lines | 13 |
| SHA-256 prefix | ed8bfa064f74d3f9 |
| First line | # 08-query-execution |
| Last line | ``` |
| Requirement-like lines | 2 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # 08-query-execution |

### EOIP-engg-doc-pkg/diagrams/09-graphrag.md

| Property | Value |
| --- | --- |
| Lines read | 14 |
| Nonblank lines | 13 |
| SHA-256 prefix | 0510787faaeba3f9 |
| First line | # 09-graphrag |
| Last line | ``` |
| Requirement-like lines | 1 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # 09-graphrag |

### EOIP-engg-doc-pkg/diagrams/10-agent-runtime.md

| Property | Value |
| --- | --- |
| Lines read | 18 |
| Nonblank lines | 17 |
| SHA-256 prefix | 34383ce35fa2b472 |
| First line | # 10-agent-runtime |
| Last line | ``` |
| Requirement-like lines | 6 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # 10-agent-runtime |

### EOIP-engg-doc-pkg/diagrams/11-multi-agent-orchestration.md

| Property | Value |
| --- | --- |
| Lines read | 17 |
| Nonblank lines | 16 |
| SHA-256 prefix | 1e88f82099e5e7da |
| First line | # 11-multi-agent-orchestration |
| Last line | ``` |
| Requirement-like lines | 1 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # 11-multi-agent-orchestration |

### EOIP-engg-doc-pkg/diagrams/12-mcp-architecture.md

| Property | Value |
| --- | --- |
| Lines read | 12 |
| Nonblank lines | 11 |
| SHA-256 prefix | 7af6721c67e1ed4a |
| First line | # 12-mcp-architecture |
| Last line | ``` |
| Requirement-like lines | 3 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # 12-mcp-architecture |

### EOIP-engg-doc-pkg/diagrams/13-human-control-architecture.md

| Property | Value |
| --- | --- |
| Lines read | 13 |
| Nonblank lines | 12 |
| SHA-256 prefix | 62be85ba2c9a6bd6 |
| First line | # 13-human-control-architecture |
| Last line | ``` |
| Requirement-like lines | 4 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # 13-human-control-architecture |

### EOIP-engg-doc-pkg/diagrams/14-web-ui-architecture.md

| Property | Value |
| --- | --- |
| Lines read | 14 |
| Nonblank lines | 13 |
| SHA-256 prefix | f11f4edb2ed1f5df |
| First line | # 14-web-ui-architecture |
| Last line | ``` |
| Requirement-like lines | 9 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # 14-web-ui-architecture |

### EOIP-engg-doc-pkg/diagrams/15-vscode-architecture.md

| Property | Value |
| --- | --- |
| Lines read | 12 |
| Nonblank lines | 11 |
| SHA-256 prefix | 51803364d8f3c76b |
| First line | # 15-vscode-architecture |
| Last line | ``` |
| Requirement-like lines | 5 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # 15-vscode-architecture |

### EOIP-engg-doc-pkg/diagrams/16-deployment.md

| Property | Value |
| --- | --- |
| Lines read | 21 |
| Nonblank lines | 20 |
| SHA-256 prefix | 8cf441ee2cbbe9e5 |
| First line | # 16-deployment |
| Last line | ``` |
| Requirement-like lines | 6 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # 16-deployment |

### EOIP-engg-doc-pkg/diagrams/17-mvp-e2e-flow.md

| Property | Value |
| --- | --- |
| Lines read | 22 |
| Nonblank lines | 21 |
| SHA-256 prefix | e5e469cde30763ee |
| First line | # 17-mvp-e2e-flow |
| Last line | ``` |
| Requirement-like lines | 3 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # 17-mvp-e2e-flow |

### EOIP-engg-doc-pkg/DOCUMENTATION-INDEX.md

| Property | Value |
| --- | --- |
| Lines read | 101 |
| Nonblank lines | 95 |
| SHA-256 prefix | e492b6fae9836855 |
| First line | # Documentation Index |
| Last line | - `examples/*` — synthetic demo fixtures. |
| Requirement-like lines | 40 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Documentation Index |
| 11 | ## Normative documents |
| 94 | ## Supporting assets |

### EOIP-engg-doc-pkg/examples/demo_documentation.md

| Property | Value |
| --- | --- |
| Lines read | 3 |
| Nonblank lines | 2 |
| SHA-256 prefix | 66c5a2431dd62e82 |
| First line | # EOIP-123 Impact Analysis |
| Last line | The impact endpoint computes a bounded dependency blast radius for a canonical code symbol and returns the evidence paths that caused each impacted item to be included. |
| Requirement-like lines | 0 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen | EOIP-123 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP-123 Impact Analysis |

### EOIP-engg-doc-pkg/gaps-implementation.md

| Property | Value |
| --- | --- |
| Lines read | 1216 |
| Nonblank lines | 965 |
| SHA-256 prefix | 48286e54a0776ce4 |
| First line | # gaps-implementation.md |
| Last line | This creates a product that can be sold earlier while preserving a path toward the broader platform vision. |
| Requirement-like lines | 183 |
| Status/gap/risk-like lines | 65 |
| Requirement IDs seen | GAP-AGOV-001..004, GAP-AGOV-001..012, GAP-AKO-001..010, GAP-APP-001..002, GAP-ARCH-001..006, GAP-CACHE-001..005, GAP-CATALOG-001..005, GAP-CHANGE-001..006, GAP-CONTRACT-001..006, GAP-CP-001..009, GAP-DATAOPS-001, GAP-DBAGNOSTIC-001, GAP-EXT-001, GAP-FABRIC-001..008, GAP-FED-001..004, GAP-FRESH-001..005, GAP-GDS-001..002, GAP-GITOPS-001..008, GAP-GOV-001..003, GAP-GRAG-001..006, GAP-HA-001, GAP-HG-001, GAP-HG-002..005, GAP-KFW-001..008, GAP-KP-001..005, GAP-KQ-001..006, GAP-KRAG-001, GAP-KRAG-001..010, GAP-LAYER-001..002, GAP-LIN-001..005, GAP-LITE-001..002, GAP-MKT-001..008, GAP-OBS-001..005, GAP-OFFLINE-001, GAP-PORT-001, GAP-PROV-001..006, GAP-QI-001..008, GAP-QI-007, GAP-RET-001..006, GAP-SDT-001..004 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # gaps-implementation.md |
| 2 | ## Phase-by-Phase Implementation Plan for Competitive Gap Closure |
| 12 | # 1. Implementation Strategy |
| 24 | # 2. Phase Map |
| 41 | # 3. Phase 0 — Architecture Foundation |
| 43 | ## Goal |
| 46 | ## Duration |
| 49 | ## Requirements |
| 57 | ## Deliverables |
| 59 | ### 3.1 Canonical Contracts |
| 79 | ### 3.2 Core IDs |
| 86 | ### 3.3 Service Boundaries |
| 119 | ### 3.4 HugeGraph Repository Abstraction |
| 131 | ### 3.5 CI Baseline |
| 140 | ## Exit Criteria |
| 150 | # 4. Phase 1 — Fully Functional Demonstrable MVP |
| 152 | ## Goal |
| 155 | ## Core Use Case |
| 164 | ## Requirements |
| 174 | ## Workstreams |
| 176 | ### 4.1 HugeGraph |
| 187 | ### 4.2 Jira Connector |
| 194 | ### 4.3 Git/Code Connector |
| 202 | ### 4.4 Cross-Link Engine |
| 212 | ### 4.5 Provenance |
| 222 | ### 4.6 Query API |
| 232 | ### 4.7 User Web |
| 239 | ### 4.8 Admin Web |
| 246 | ### 4.9 VS Code |
| 253 | ### 4.10 GraphRAG |
| 259 | ### 4.11 MCP |
| 268 | ## Tests |
| 280 | ## Demo Exit Criteria |
| 285 | # 5. Phase 2 — Trustworthy Ontology & Semantic Governance |
| 287 | ## Goal |
| 290 | ## Requirements |
| 300 | ## 5.1 Ontology-as-Code |
| 324 | ## 5.2 Semantic Diff Engine |
| 333 | ## 5.3 Ontology CI |
| 344 | ## 5.4 Ontology Studio |
| 354 | ## 5.5 Claim/Truth Model |
| 363 | ## 5.6 Trust Zones |
| 367 | ## Exit Criteria |
| 375 | # 6. Phase 3 — Enterprise Engineering Intelligence |
| 377 | ## Goal |
| 380 | ## Requirements |
| 388 | ## 6.1 Deep Code Graph |
| 402 | ## 6.2 CI/CD Graph |
| 412 | ## 6.3 Runtime/ITSM Graph |
| 422 | ## 6.4 Architecture Conformance DSL |
| 434 | ## 6.5 Pre-Merge Impact |
| 442 | ## 6.6 Documentation Freshness |
| 446 | ## Exit Criteria |
| 452 | # 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG |
| 454 | ## Goal |
| 457 | ## Requirements |
| 465 | ## 7.1 Retrieval Router |
| 484 | ## 7.2 Full Text |
| 490 | ## 7.3 Vector |
| 495 | ## 7.4 GraphRAG Evaluation Harness |
| 521 | ## 7.5 Community Summaries |
| 525 | ## Exit Criteria |
| 530 | # 8. Phase 5 — Federation, Catalog & Knowledge Products |
| 532 | ## Goal |
| 535 | ## Requirements |
| 544 | ## 8.1 Federation Architecture |
| 562 | ## 8.2 Materialization Policy |
| 569 | ## 8.3 Knowledge Catalog |
| 581 | ## 8.4 Knowledge Products |
| 590 | ## Exit Criteria |
| 595 | # 9. Phase 6 — Governed Agentic Knowledge Operations |
| 597 | ## Goal |
| 600 | ## Requirements |
| 606 | ## 9.1 Agent Runtime |
| 618 | ## 9.2 Tool Risk Classes |
| 627 | ## 9.3 Initial Agents |
| 636 | ## 9.4 Knowledge Firewall |
| 643 | ## 9.5 Evaluation |
| 652 | ## Exit Criteria |
| 657 | # 10. Phase 7 — Enterprise Security, HA & Operational Maturity |
| 659 | ## Goal |
| 662 | ## Requirements |
| 669 | ## 10.1 Identity |
| 676 | ## 10.2 Authorization |
| 685 | ## 10.3 HugeGraph Distributed |
| 696 | ## 10.4 HA Application Layer |
| 703 | ## 10.5 DR |
| 711 | ## 10.6 Enterprise Operations |
| 720 | ## Exit Criteria |
| 725 | # 11. Phase 8 — Advanced Analytics, Simulation & Predictive Intelligence |
| 727 | ## Goal |
| 730 | ## Requirements |
| 735 | ## 11.1 Analytics |
| 745 | ## 11.2 Risk Model |
| 758 | ## 11.3 What-If Sandbox |
| 767 | ## 11.4 Calibration |
| 771 | ## Exit Criteria |
| 776 | # 12. Phase 9 — Ecosystem, Extensions & Domain Packs |
| 778 | ## Goal |
| 781 | ## Requirements |
| 788 | ## 12.1 SDKs |
| 801 | ## 12.2 Package Manifest |
| 818 | ## 12.3 Signing |
| 824 | ## 12.4 App Builder |
| 837 | # 13. Cross-Phase Architecture Components |
| 839 | ## Always Present |
| 855 | # 14. Data Migration Strategy |
| 876 | # 15. Testing Evolution by Phase |
| 878 | ## Phase 1 |
| 881 | ## Phase 2 |
| 884 | ## Phase 3 |
| 887 | ## Phase 4 |
| 890 | ## Phase 5 |
| 893 | ## Phase 6 |
| 896 | ## Phase 7 |
| 899 | ## Phase 8 |
| 902 | ## Phase 9 |
| 907 | # 16. Recommended Release Gates |
| 911 | ### Gate A — Data |
| 915 | ### Gate B — Graph |
| 919 | ### Gate C — Security |
| 924 | ### Gate D — AI |
| 928 | ### Gate E — Operations |
| 934 | # 17. Performance Engineering |
| 938 | ### S |
| 941 | ### M |
| 944 | ### L |
| 947 | ### XL |
| 967 | # 18. Technology Decisions |
| 969 | ## Keep |
| 982 | ## Add Carefully |
| 992 | # 19. Implementation Ordering Inside Each Phase |
| 1011 | # 20. Definition of Done for Every Gap Requirement |
| 1028 | # 21. Suggested Milestone Sequence |
| 1030 | ## M0 — Foundation |
| 1033 | ## M1 — Connected Graph MVP |
| 1036 | ## M2 — Evidence |
| 1039 | ## M3 — UX |
| 1042 | ## M4 — Semantic Governance |
| 1045 | ## M5 — Engineering Intelligence |
| 1048 | ## M6 — Trusted AI |
| 1051 | ## M7 — Federation |
| 1054 | ## M8 — Governed Agents |
| 1057 | ## M9 — Enterprise |
| 1060 | ## M10 — Analytics/Ecosystem |
| 1065 | # 22. Commercial Pilot Readiness |
| 1087 | # 23. Enterprise GA Readiness |
| 1106 | # 24. “Competitor Con → Our Pro” Mapping |
| 1128 | # 25. Delivery Backlog Structure |
| 1159 | # 26. Recommended First 90-Day Build Focus |
| 1163 | ### Days 1–30 |
| 1171 | ### Days 31–60 |
| 1179 | ### Days 61–90 |
| 1191 | # 27. Architecture Rule |
| 1203 | # 28. Final Implementation Principle |

### EOIP-engg-doc-pkg/gaps-requirements.md

| Property | Value |
| --- | --- |
| Lines read | 1401 |
| Nonblank lines | 1063 |
| SHA-256 prefix | 76ed4843e3f32f69 |
| First line | # gaps-requirements.md |
| Last line |  |
| Requirement-like lines | 313 |
| Status/gap/risk-like lines | 294 |
| Requirement IDs seen | GAP-AGOV-001, GAP-AGOV-002, GAP-AGOV-003, GAP-AGOV-004, GAP-AGOV-005, GAP-AGOV-006, GAP-AGOV-007, GAP-AGOV-008, GAP-AGOV-009, GAP-AGOV-010, GAP-AGOV-011, GAP-AGOV-012, GAP-AI-001, GAP-AKO-001, GAP-AKO-002, GAP-AKO-003, GAP-AKO-004, GAP-AKO-005, GAP-AKO-006, GAP-AKO-007, GAP-AKO-008, GAP-AKO-009, GAP-AKO-010, GAP-APP-001, GAP-APP-002, GAP-ARCH-001, GAP-ARCH-002, GAP-ARCH-003, GAP-ARCH-004, GAP-ARCH-005, GAP-ARCH-006, GAP-CACHE-001, GAP-CACHE-002, GAP-CACHE-003, GAP-CACHE-004, GAP-CACHE-005, GAP-CATALOG-001, GAP-CATALOG-002, GAP-CATALOG-003, GAP-CATALOG-004 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # gaps-requirements.md |
| 2 | ## Enterprise Ontology & Knowledge Intelligence Platform — Competitive Gap Requirements |
| 15 | ## 1. Purpose |
| 41 | # 2. Existing Baseline Already Covered |
| 67 | # 3. Research Method |
| 98 | # 4. Competitive Study |
| 100 | ## 4.1 Stardog |
| 102 | ### Documented strengths |
| 110 | ### Trade-offs relative to our target |
| 116 | ### Requirements to turn these trade-offs into strengths |
| 125 | ## 4.2 Neo4j |
| 127 | ### Documented strengths |
| 134 | ### Trade-offs relative to our target |
| 141 | ### Requirements |
| 151 | ## 4.3 Ontotext GraphDB |
| 153 | ### Documented strengths |
| 161 | ### Trade-offs relative to our target |
| 167 | ### Requirements |
| 177 | ## 4.4 TopBraid EDG / TQ Data Foundation |
| 179 | ### Documented strengths |
| 187 | ### Trade-offs relative to our target |
| 193 | ### Requirements |
| 204 | ## 4.5 PoolParty Semantic Suite |
| 206 | ### Documented strengths |
| 214 | ### Trade-offs relative to our target |
| 220 | ### Requirements |
| 229 | ## 4.6 Cambridge Semantics Anzo / Graph Studio |
| 231 | ### Documented strengths |
| 238 | ### Trade-offs relative to our target |
| 244 | ### Requirements |
| 259 | ## 4.7 metaphactory |
| 261 | ### Documented strengths |
| 267 | ### Trade-offs relative to our target |
| 272 | ### Requirements |
| 280 | ## 4.8 data.world |
| 282 | ### Documented strengths |
| 290 | ### Trade-offs relative to our target |
| 295 | ### Requirements |
| 304 | ## 4.9 Amazon Neptune |
| 306 | ### Documented strengths |
| 312 | ### Trade-offs relative to our target |
| 318 | ### Requirements |
| 326 | ## 4.10 Oracle RDF Graph |
| 328 | ### Documented strengths |
| 332 | ### Trade-offs relative to our target |
| 337 | ### Requirements |
| 344 | ## 4.11 Microsoft GraphRAG |
| 346 | ### Documented strengths |
| 352 | ### Documented cautions |
| 357 | ### Requirements |
| 367 | # 5. Highest-Value Gaps to Add |
| 373 | # 6. Semantic Digital Thread |
| 375 | ## Objective |
| 379 | ## Requirements |
| 390 | ### Acceptance |
| 395 | # 7. Enterprise Semantic Control Plane |
| 397 | ## Requirements |
| 411 | # 8. Ontology GitOps / Semantic DevOps |
| 415 | ## Requirements |
| 435 | # 9. Semantic Contract Testing |
| 437 | ## Requirements |
| 448 | # 10. Provenance & Evidence Ledger |
| 452 | ## Requirements |
| 466 | # 11. Confidence, Contradiction & Truth Management |
| 468 | ## Requirements |
| 483 | # 12. Knowledge Quality SLOs |
| 487 | ## Requirements |
| 509 | # 13. Semantic Drift Detection |
| 511 | ## Requirements |
| 523 | # 14. Architecture Conformance Engine |
| 527 | ## Requirements |
| 543 | # 15. Change Intelligence & Semantic Blast Radius |
| 545 | ## Requirements |
| 564 | # 16. Temporal / Bitemporal Knowledge |
| 566 | ## Requirements |
| 577 | # 17. Knowledge Catalog & Knowledge Products |
| 579 | ## Requirements |
| 599 | # 18. Ontology Studio & Collaborative Knowledge Engineering |
| 601 | ## Requirements |
| 617 | # 19. Enterprise Entity Resolution Workbench |
| 619 | ## Requirements |
| 634 | # 20. Federated Knowledge Fabric |
| 636 | ## Requirements |
| 649 | # 21. Unified Retrieval Fabric |
| 651 | ## Requirements |
| 672 | # 22. Knowledge-Aware GraphRAG |
| 674 | ## Requirements |
| 689 | # 23. Agentic Knowledge Operations |
| 691 | ## Requirements |
| 710 | # 24. Agent & MCP Governance |
| 712 | ## Requirements |
| 729 | # 25. Knowledge Firewall |
| 733 | ## Requirements |
| 746 | # 26. Knowledge Quarantine & Trust Zones |
| 748 | ## Requirements |
| 765 | # 27. Fine-Grained Security Roadmap |
| 787 | # 28. Data & Knowledge Lineage Interoperability |
| 789 | ## Requirements |
| 799 | # 29. Graph Change Data Capture |
| 801 | ## Requirements |
| 812 | # 30. Knowledge Graph CI/CD |
| 814 | ## Requirements |
| 827 | # 31. Graph Testing Framework |
| 829 | ## Requirements |
| 849 | # 32. Graph Observability |
| 853 | ## Requirements |
| 869 | # 33. Query Intelligence |
| 871 | ## Requirements |
| 884 | # 34. Semantic Cache |
| 886 | ## Requirements |
| 896 | # 35. Knowledge Compaction & Lifecycle |
| 898 | ## Requirements |
| 909 | # 36. Schema & Mapping Marketplace |
| 913 | ## Requirements |
| 926 | # 37. Domain Packs |
| 945 | # 38. Enterprise Search Experience |
| 947 | ## Requirements |
| 975 | # 39. Expert Finder / Organizational Knowledge |
| 977 | ## Requirements |
| 997 | # 40. Knowledge Freshness Engine |
| 999 | ## Requirements |
| 1009 | # 41. Semantic Diff & Release Intelligence |
| 1011 | ## Requirements |
| 1027 | # 42. Graph Simulation / What-If Engine |
| 1029 | ## Requirements |
| 1045 | # 43. Knowledge Graph Benchmark Harness |
| 1047 | ## Requirements |
| 1068 | # 44. HugeGraph-Specific Hardening |
| 1072 | ## Requirements |
| 1087 | # 45. Product Extensibility |
| 1089 | ## Requirements |
| 1108 | # 46. Enterprise Packaging |
| 1112 | ### Developer |
| 1115 | ### Team |
| 1118 | ### Enterprise |
| 1121 | ### Air-Gapped |
| 1126 | # 47. Operational Excellence |
| 1142 | # 48. Security Beyond MVP |
| 1162 | # 49. Responsible AI & Model Governance |
| 1164 | ## Requirements |
| 1182 | # 50. Explainability Without Chain-of-Thought |
| 1198 | # 51. “Why / Why Not / What If” Native Queries |
| 1215 | # 52. Requirement Priority |
| 1217 | ## P0 — Core differentiation |
| 1234 | ## P1 — Enterprise maturity |
| 1248 | ## P2 — Advanced differentiation |
| 1260 | # 53. Commercial Differentiators to Target |
| 1282 | # 54. Requirements Traceability Template |
| 1294 | # 55. Non-Functional Targets |
| 1317 | # 56. Important Product Principle |
| 1329 | # 57. Research References |
| 1387 | # 58. Final Requirement |

### EOIP-engg-doc-pkg/gaps2-implementation.md

| Property | Value |
| --- | --- |
| Lines read | 1625 |
| Nonblank lines | 1142 |
| SHA-256 prefix | 610101b8885c55b8 |
| First line | # gaps2-implementation.md |
| Last line | This order turns EOIP into a trustworthy live enterprise knowledge twin rather than a visually impressive but unreliable graph demo. |
| Requirement-like lines | 155 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen | G2-ADMIN-001..017, G2-ARCH-001..015, G2-ARCHC-001..009, G2-CAP-001..006, G2-CAUSE-001..006, G2-EKAF-001..030, G2-EKAF-003, G2-EVENT-001, G2-EVENT-001..007, G2-EVOL-001..016, G2-EVOL-009, G2-GRAPH-API-001..003, G2-GRAPH-OBS-001..003, G2-GRAPH-RUNTIME-001..003, G2-GRAPH-SEC-001..003, G2-I2R-001..005, G2-IMMUNE-001..013, G2-JOURNAL-001..006, G2-KD-001..006, G2-OBS-001..002, G2-OEVO-001..006, G2-PM-001..005, G2-QOP-001..009, G2-QOP-003, G2-REL-001..008, G2-SEC-CRAWL-001..012, G2-SIM-001..007, G2-SLO-001..005, G2-SRC-API-001..006, G2-SRC-CICD-001..004, G2-SRC-CODE-001..005, G2-SRC-CONF-001..005, G2-SRC-DD-001..004, G2-SRC-GH-001..004, G2-SRC-GL-001..004, G2-SRC-GRAF-001..003, G2-SRC-JIRA-001..006, G2-SRC-KIB-001..005, G2-SRC-OTEL-001..005, G2-SRC-RUNTIME-001..003 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # gaps2-implementation.md |
| 2 | ## EOIP — Phase-by-Phase Implementation Plan for Enterprise Knowledge Acquisition, Graph Evolution & Next-Generation Intelligence |
| 12 | # 1. Implementation Objective |
| 31 | # 2. Phase Overview |
| 51 | # 3. G2-P0 — Contract & Architecture Alignment |
| 53 | ## Goal |
| 56 | ## Requirements |
| 62 | ## Tasks |
| 64 | ### G2-T0001 — Audit current contracts |
| 78 | ### G2-T0002 — SourceEvent v2 |
| 90 | ### G2-T0003 — Canonical revision model |
| 102 | ### G2-T0004 — Source Registry schema |
| 105 | ### G2-T0005 — Capability interfaces |
| 119 | ### G2-T0006 — Traceability |
| 122 | ## Tests |
| 128 | ## Exit Criteria |
| 133 | # 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core |
| 135 | ## Goal |
| 138 | ## Requirements |
| 143 | ## Workstream A — Source Registry |
| 145 | ### G2-T0101 |
| 148 | ### G2-T0102 |
| 151 | ### G2-T0103 |
| 154 | ### G2-T0104 |
| 159 | ## Workstream B — Scheduler |
| 161 | ### G2-T0110 |
| 170 | ### G2-T0111 |
| 173 | ### G2-T0112 |
| 178 | ## Workstream C — Webhook Gateway |
| 180 | ### G2-T0120 |
| 183 | ### G2-T0121 |
| 186 | ### G2-T0122 |
| 189 | ### G2-T0123 |
| 194 | ## Workstream D — Controlled Web Crawler |
| 196 | ### G2-T0130 |
| 205 | ### G2-T0131 |
| 208 | ### G2-T0132 |
| 216 | ### G2-T0133 |
| 219 | ### G2-T0134 |
| 222 | ### G2-T0135 |
| 227 | ## Workstream E — DLQ / Replay |
| 229 | ### G2-T0140 |
| 232 | ### G2-T0141 |
| 235 | ### G2-T0142 |
| 240 | ## Workstream F — Discovery / Dry Run |
| 242 | ### G2-T0150 |
| 245 | ### G2-T0151 |
| 248 | ### G2-T0152 |
| 251 | ### G2-T0153 |
| 256 | ## Exit Criteria |
| 261 | # 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution |
| 263 | ## Goal |
| 266 | ## Requirements |
| 275 | ## Workstream A — Baseline Controller |
| 277 | ### G2-T0201 |
| 282 | ### G2-T0202 |
| 291 | ### G2-T0203 |
| 296 | ## Workstream B — Incremental Change Detector |
| 298 | ### G2-T0210 |
| 301 | ### G2-T0211 |
| 304 | ### G2-T0212 |
| 312 | ### G2-T0213 |
| 317 | ## Workstream C — Graph Evolution Engine |
| 319 | ### G2-T0220 |
| 322 | ### G2-T0221 |
| 330 | ### G2-T0222 |
| 333 | ### G2-T0223 |
| 336 | ### G2-T0224 |
| 339 | ### G2-T0225 |
| 344 | ## Workstream D — Semantic Change Journal |
| 346 | ### G2-T0230 |
| 349 | ### G2-T0231 |
| 352 | ### G2-T0232 |
| 357 | ## Workstream E — Semantic Event Bus |
| 359 | ### G2-T0240 |
| 362 | ### G2-T0241 |
| 365 | ### G2-T0242 |
| 371 | ### G2-T0243 |
| 376 | ## Workstream F — Reconciliation |
| 378 | ### G2-T0250 |
| 381 | ### G2-T0251 |
| 384 | ### G2-T0252 |
| 387 | ### G2-T0253 |
| 392 | ## Critical Tests |
| 405 | ## Exit Criteria |
| 410 | # 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files |
| 412 | ## Goal |
| 415 | ## Requirements |
| 424 | ## 6.1 Jira |
| 426 | ### G2-T0301 |
| 433 | ### G2-T0302 |
| 436 | ### G2-T0303 |
| 439 | ### G2-T0304 |
| 444 | ## 6.2 GitLab |
| 446 | ### G2-T0310 |
| 449 | ### G2-T0311 |
| 452 | ### G2-T0312 |
| 455 | ### G2-T0313 |
| 460 | ## 6.3 GitHub |
| 462 | ### G2-T0320 |
| 465 | ### G2-T0321 |
| 468 | ### G2-T0322 |
| 471 | ### G2-T0323 |
| 476 | ## 6.4 Code Incremental Parsing |
| 478 | ### G2-T0330 |
| 481 | ### G2-T0331 |
| 484 | ### G2-T0332 |
| 487 | ### G2-T0333 |
| 492 | ## 6.5 Generic file/web |
| 494 | ### G2-T0340 |
| 497 | ### G2-T0341 |
| 500 | ### G2-T0342 |
| 505 | ## Demo |
| 514 | # 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals |
| 516 | ## Goal |
| 519 | ## Requirements |
| 528 | ## 7.1 Confluence |
| 530 | ### G2-T0401 |
| 533 | ### G2-T0402 |
| 536 | ### G2-T0403 |
| 539 | ### G2-T0404 |
| 542 | ### G2-T0405 |
| 547 | ## 7.2 ServiceNow |
| 551 | ### G2-T0410 — KB |
| 554 | ### G2-T0411 — Incident |
| 557 | ### G2-T0412 — Problem |
| 560 | ### G2-T0413 — Change |
| 563 | ### G2-T0414 — CMDB |
| 566 | ### G2-T0415 |
| 569 | ### G2-T0416 |
| 574 | ## 7.3 API Portal / Contracts |
| 576 | ### G2-T0420 |
| 579 | ### G2-T0421 |
| 582 | ### G2-T0422 |
| 585 | ### G2-T0423 |
| 588 | ### G2-T0424 |
| 591 | ### G2-T0425 |
| 594 | ### G2-T0426 |
| 599 | ## Exit Criteria |
| 605 | # 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM |
| 607 | ## Goal |
| 610 | ## Requirements |
| 625 | ## 8.1 CI/CD |
| 627 | ### G2-T0501 |
| 630 | ### G2-T0502 |
| 633 | ### G2-T0503 |
| 636 | ### G2-T0504 |
| 641 | ## 8.2 Kibana |
| 643 | ### G2-T0510 |
| 646 | ### G2-T0511 |
| 649 | ### G2-T0512 |
| 652 | ### G2-T0513 |
| 657 | ## 8.3 Datadog |
| 659 | ### G2-T0520 |
| 662 | ### G2-T0521 |
| 665 | ### G2-T0522 |
| 668 | ### G2-T0523 |
| 673 | ## 8.4 Grafana |
| 675 | ### G2-T0530 |
| 678 | ### G2-T0531 |
| 681 | ### G2-T0532 |
| 686 | ## 8.5 OpenTelemetry |
| 688 | ### G2-T0540 |
| 691 | ### G2-T0541 |
| 694 | ### G2-T0542 |
| 697 | ### G2-T0543 |
| 702 | ## 8.6 Runtime |
| 704 | ### G2-T0550 |
| 707 | ### G2-T0551 |
| 712 | ## 8.7 SBOM |
| 714 | ### G2-T0560 |
| 717 | ### G2-T0561 |
| 720 | ### G2-T0562 |
| 723 | ### G2-T0563 |
| 728 | ## Critical Guardrail |
| 733 | # 9. G2-P6 — Expanded Semantic Digital Twin |
| 735 | ## Goal |
| 738 | ## Requirements |
| 752 | ## Workstream A — Test Intelligence |
| 754 | ### G2-T0601 |
| 757 | ### G2-T0602 |
| 760 | ### G2-T0603 |
| 765 | ## Workstream B — Decision Graph |
| 767 | ### G2-T0610 |
| 770 | ### G2-T0611 |
| 773 | ### G2-T0612 |
| 778 | ## Workstream C — Business Intent |
| 780 | ### G2-T0620 |
| 783 | ### G2-T0621 |
| 786 | ### G2-T0622 |
| 791 | ## Workstream D — Digital Twin View |
| 793 | ### G2-T0630 |
| 800 | ### G2-T0631 |
| 803 | ### G2-T0632 |
| 808 | ## Exit Criteria |
| 814 | # 10. G2-P7 — Temporal, Architecture & Process Intelligence |
| 816 | ## Goal |
| 819 | ## Requirements |
| 829 | ## 10.1 Enterprise Time Machine |
| 831 | ### G2-T0701 |
| 834 | ### G2-T0702 |
| 837 | ### G2-T0703 |
| 840 | ### G2-T0704 |
| 843 | ### G2-T0705 |
| 848 | ## 10.2 Architecture Conformance |
| 850 | ### G2-T0710 |
| 853 | ### G2-T0711 |
| 856 | ### G2-T0712 |
| 859 | ### G2-T0713 |
| 862 | ### G2-T0714 |
| 865 | ### G2-T0715 |
| 870 | ## 10.3 Process Mining |
| 872 | ### G2-T0720 |
| 875 | ### G2-T0721 |
| 878 | ### G2-T0722 |
| 881 | ### G2-T0723 |
| 886 | ## 10.4 Knowledge Debt |
| 888 | ### G2-T0730 |
| 891 | ### G2-T0731 |
| 894 | ### G2-T0732 |
| 897 | ### G2-T0733 |
| 902 | ## 10.5 Knowledge SLO |
| 904 | ### G2-T0740 |
| 907 | ### G2-T0741 |
| 910 | ### G2-T0742 |
| 913 | ### G2-T0743 |
| 918 | ## 10.6 Native Query Operators |
| 920 | ### G2-T0750 |
| 923 | ### G2-T0751 |
| 926 | ### G2-T0752 |
| 929 | ### G2-T0753 |
| 936 | # 11. G2-P8 — Knowledge Health & Governed AI |
| 938 | ## Goal |
| 941 | ## Requirements |
| 948 | ## 11.1 Knowledge Immune System |
| 950 | ### G2-T0801 |
| 953 | ### G2-T0802 |
| 956 | ### G2-T0803 |
| 959 | ### G2-T0804 |
| 962 | ### G2-T0805 |
| 967 | ## 11.2 Ontology Evolution Proposals |
| 969 | ### G2-T0810 |
| 972 | ### G2-T0811 |
| 975 | ### G2-T0812 |
| 978 | ### G2-T0813 |
| 981 | ### G2-T0814 |
| 986 | ## 11.3 Knowledge Capsules |
| 988 | ### G2-T0820 |
| 991 | ### G2-T0821 |
| 994 | ### G2-T0822 |
| 997 | ### G2-T0823 |
| 1000 | ### G2-T0824 |
| 1005 | ## Exit Criteria |
| 1010 | # 12. G2-P9 — Counterfactual Twin & Causal Intelligence |
| 1012 | ## Goal |
| 1015 | ## Requirements |
| 1022 | ## 12.1 Simulation Workspace |
| 1024 | ### G2-T0901 |
| 1027 | ### G2-T0902 |
| 1030 | ### G2-T0903 |
| 1033 | ### G2-T0904 |
| 1036 | ### G2-T0905 |
| 1039 | ### G2-T0906 |
| 1044 | ## 12.2 What-If Operator |
| 1046 | ### G2-T0910 |
| 1049 | ### G2-T0911 |
| 1052 | ### G2-T0912 |
| 1057 | ## 12.3 Causal Hypothesis Engine |
| 1059 | ### G2-T0920 |
| 1062 | ### G2-T0921 |
| 1065 | ### G2-T0922 |
| 1068 | ### G2-T0923 |
| 1071 | ### G2-T0924 |
| 1076 | ## Validation |
| 1081 | # 13. G2-P10 — Diamond-Standard UX & Production Hardening |
| 1083 | ## Goal |
| 1086 | ## Requirements |
| 1096 | ## 13.1 Lens Framework |
| 1115 | ## 13.2 Required Lens Delivery Order |
| 1140 | ## 13.3 Graph Canvas |
| 1152 | ## 13.4 Graph Playback |
| 1154 | ### G2-T1030 |
| 1157 | ### G2-T1031 |
| 1160 | ### G2-T1032 |
| 1163 | ### G2-T1033 |
| 1168 | ## 13.5 Production Hardening |
| 1170 | ### G2-T1040 |
| 1173 | ### G2-T1041 |
| 1176 | ### G2-T1042 |
| 1179 | ### G2-T1043 |
| 1182 | ### G2-T1044 |
| 1185 | ### G2-T1045 |
| 1188 | ### G2-T1046 |
| 1193 | # 14. Cross-Phase Source Adapter Template |
| 1216 | # 15. Connector Implementation Checklist |
| 1249 | # 16. Graph Evolution Mutation Algorithm |
| 1294 | # 17. Historical Relationship Strategy |
| 1317 | # 18. Telemetry Aggregation Strategy |
| 1319 | ## Logs |
| 1330 | ## Metrics |
| 1338 | ## Traces |
| 1350 | # 19. Versioning Strategy |
| 1368 | # 20. Recommended Persistence Additions |
| 1386 | # 21. UI Delivery Principle |
| 1400 | # 22. AI Use by Phase |
| 1402 | ## P0–P5 |
| 1405 | ## P6–P7 |
| 1411 | ## P8 |
| 1417 | ## P9 |
| 1424 | # 23. Test Matrix |
| 1443 | # 24. Phase Exit Gates |
| 1445 | ## Gate 0 — Contract Integrity |
| 1448 | ## Gate 1 — Acquisition Integrity |
| 1451 | ## Gate 2 — Incremental Integrity |
| 1454 | ## Gate 3 — Engineering Sources |
| 1457 | ## Gate 4 — Enterprise Sources |
| 1460 | ## Gate 5 — Runtime Knowledge |
| 1463 | ## Gate 6 — Digital Twin |
| 1466 | ## Gate 7 — Temporal Intelligence |
| 1469 | ## Gate 8 — Knowledge Health |
| 1472 | ## Gate 9 — Simulation |
| 1475 | ## Gate 10 — UX/Operations |
| 1480 | # 25. Commercial Pilot Subset |
| 1517 | # 26. First Recommended Implementation Sprint Sequence |
| 1519 | ## Sprint/Iteration 1 |
| 1522 | ## Sprint/Iteration 2 |
| 1525 | ## Sprint/Iteration 3 |
| 1528 | ## Sprint/Iteration 4 |
| 1531 | ## Sprint/Iteration 5 |
| 1534 | ## Sprint/Iteration 6 |
| 1537 | ## Sprint/Iteration 7 |
| 1540 | ## Sprint/Iteration 8 |
| 1543 | ## Sprint/Iteration 9 |
| 1546 | ## Sprint/Iteration 10 |
| 1553 | # 27. AI Coding Agent Work Protocol |
| 1579 | # 28. Definition of Done |
| 1597 | # 29. Final Build Order Principle |

### EOIP-engg-doc-pkg/gaps2-requirements.md

| Property | Value |
| --- | --- |
| Lines read | 2059 |
| Nonblank lines | 1500 |
| SHA-256 prefix | dfb9b47bbf3cfb25 |
| First line | # gaps2-requirements.md |
| Last line | EOIP's target end state is a **continuously synchronized, time-aware, evidence-backed digital knowledge twin of the enterprise** that can be queried, compared, simulated and safely consumed by humans and AI systems. |
| Requirement-like lines | 397 |
| Status/gap/risk-like lines | 3 |
| Requirement IDs seen | G2-ADMIN-001, G2-ADMIN-002, G2-ADMIN-003, G2-ADMIN-004, G2-ADMIN-005, G2-ADMIN-006, G2-ADMIN-007, G2-ADMIN-008, G2-ADMIN-009, G2-ADMIN-010, G2-ADMIN-011, G2-ADMIN-012, G2-ADMIN-013, G2-ADMIN-014, G2-ADMIN-015, G2-ADMIN-016, G2-ADMIN-017, G2-ARCH-001, G2-ARCH-002, G2-ARCH-003, G2-ARCH-004, G2-ARCH-005, G2-ARCH-006, G2-ARCH-007, G2-ARCH-008, G2-ARCH-009, G2-ARCH-010, G2-ARCH-011, G2-ARCH-012, G2-ARCH-013, G2-ARCH-014, G2-ARCH-015, G2-ARCHC-001, G2-ARCHC-002, G2-ARCHC-003, G2-ARCHC-004, G2-ARCHC-005, G2-ARCHC-006, G2-ARCHC-007, G2-ARCHC-008 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # gaps2-requirements.md |
| 2 | ## EOIP — Enterprise Knowledge Acquisition, Graph Evolution & Next-Generation Intelligence Requirements |
| 16 | # 1. Purpose |
| 50 | # 2. Non-Negotiable Architectural Principles |
| 52 | ## G2-ARCH-001 — One acquisition contract |
| 56 | ## G2-ARCH-002 — API/event first |
| 68 | ## G2-ARCH-003 — Deterministic first |
| 72 | ## G2-ARCH-004 — Preserve source fidelity |
| 76 | ## G2-ARCH-005 — HugeGraph is semantic operational truth |
| 80 | ## G2-ARCH-006 — No raw telemetry lake in HugeGraph |
| 84 | ## G2-ARCH-007 — No destructive history overwrite |
| 88 | ## G2-ARCH-008 — Current and historical views |
| 92 | ## G2-ARCH-009 — One semantic identity system |
| 96 | ## G2-ARCH-010 — Evidence is mandatory |
| 100 | ## G2-ARCH-011 — AI is not the source of truth |
| 104 | ## G2-ARCH-012 — Incremental by default after baseline |
| 108 | ## G2-ARCH-013 — Replayability |
| 112 | ## G2-ARCH-014 — Source permissions respected |
| 116 | ## G2-ARCH-015 — Progressive complexity |
| 122 | # 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF) |
| 126 | ## 3.1 Core components |
| 153 | ## Requirements |
| 155 | ### G2-EKAF-001 — Source Registry |
| 175 | ### G2-EKAF-002 — Connector SDK |
| 187 | ### G2-EKAF-003 — SourceEvent envelope |
| 204 | ### G2-EKAF-004 — Baseline crawl |
| 207 | ### G2-EKAF-005 — Incremental sync |
| 215 | ### G2-EKAF-006 — Webhook/event ingestion |
| 218 | ### G2-EKAF-007 — Poll fallback |
| 221 | ### G2-EKAF-008 — Reconciliation crawl |
| 224 | ### G2-EKAF-009 — Idempotency |
| 227 | ### G2-EKAF-010 — Ordering tolerance |
| 230 | ### G2-EKAF-011 — Rate limiting |
| 238 | ### G2-EKAF-012 — Checkpointing |
| 241 | ### G2-EKAF-013 — Replay |
| 250 | ### G2-EKAF-014 — Dead-letter handling |
| 259 | ### G2-EKAF-015 — Dry run |
| 262 | ### G2-EKAF-016 — Source deletion semantics |
| 265 | ### G2-EKAF-017 — Schema drift |
| 272 | ### G2-EKAF-018 — Mapping drift |
| 275 | ### G2-EKAF-019 — Crawl boundaries |
| 287 | ### G2-EKAF-020 — Authentication isolation |
| 290 | ### G2-EKAF-021 — Connector health |
| 301 | ### G2-EKAF-022 — Source priority |
| 304 | ### G2-EKAF-023 — Permission-aware metadata |
| 307 | ### G2-EKAF-024 — Content fingerprinting |
| 310 | ### G2-EKAF-025 — Attachment handling |
| 319 | ### G2-EKAF-026 — Incremental graph enrichment |
| 322 | ### G2-EKAF-027 — Source capability introspection |
| 334 | ### G2-EKAF-028 — Connector compatibility matrix |
| 337 | ### G2-EKAF-029 — Offline source fixture mode |
| 340 | ### G2-EKAF-030 — Source onboarding wizard |
| 346 | # 4. Source-Specific Acquisition Requirements |
| 348 | # 4.1 Jira |
| 350 | ## G2-SRC-JIRA-001 |
| 353 | ## G2-SRC-JIRA-002 |
| 356 | ## G2-SRC-JIRA-003 |
| 359 | ## G2-SRC-JIRA-004 |
| 362 | ## G2-SRC-JIRA-005 |
| 365 | ## G2-SRC-JIRA-006 |
| 370 | # 4.2 Confluence / Enterprise Wiki |
| 372 | ## G2-SRC-CONF-001 |
| 375 | ## G2-SRC-CONF-002 |
| 378 | ## G2-SRC-CONF-003 |
| 381 | ## G2-SRC-CONF-004 |
| 384 | ## G2-SRC-CONF-005 |
| 389 | # 4.3 ServiceNow Knowledge Base |
| 391 | ## G2-SRC-SNKB-001 |
| 394 | ## G2-SRC-SNKB-002 |
| 397 | ## G2-SRC-SNKB-003 |
| 402 | # 4.4 ServiceNow Incidents / Problems / Changes / CMDB |
| 404 | ## G2-SRC-SNOW-001 |
| 407 | ## G2-SRC-SNOW-002 |
| 410 | ## G2-SRC-SNOW-003 |
| 413 | ## G2-SRC-SNOW-004 |
| 416 | ## G2-SRC-SNOW-005 |
| 419 | ## G2-SRC-SNOW-006 |
| 424 | # 4.5 GitHub |
| 426 | ## G2-SRC-GH-001 |
| 429 | ## G2-SRC-GH-002 |
| 432 | ## G2-SRC-GH-003 |
| 435 | ## G2-SRC-GH-004 |
| 440 | # 4.6 GitLab |
| 442 | ## G2-SRC-GL-001 |
| 445 | ## G2-SRC-GL-002 |
| 448 | ## G2-SRC-GL-003 |
| 451 | ## G2-SRC-GL-004 |
| 456 | # 4.7 Local Git / Source Code |
| 458 | ## G2-SRC-CODE-001 |
| 461 | ## G2-SRC-CODE-002 |
| 464 | ## G2-SRC-CODE-003 |
| 467 | ## G2-SRC-CODE-004 |
| 470 | ## G2-SRC-CODE-005 |
| 475 | # 4.8 API Portals / Contracts |
| 477 | ## G2-SRC-API-001 |
| 480 | ## G2-SRC-API-002 |
| 483 | ## G2-SRC-API-003 |
| 487 | ## G2-SRC-API-004 |
| 490 | ## G2-SRC-API-005 |
| 493 | ## G2-SRC-API-006 |
| 498 | # 4.9 Kibana / Elastic Observability |
| 500 | ## G2-SRC-KIB-001 |
| 503 | ## G2-SRC-KIB-002 |
| 506 | ## G2-SRC-KIB-003 |
| 509 | ## G2-SRC-KIB-004 |
| 519 | ## G2-SRC-KIB-005 |
| 524 | # 4.10 Datadog |
| 526 | ## G2-SRC-DD-001 |
| 529 | ## G2-SRC-DD-002 |
| 532 | ## G2-SRC-DD-003 |
| 535 | ## G2-SRC-DD-004 |
| 540 | # 4.11 Grafana |
| 542 | ## G2-SRC-GRAF-001 |
| 545 | ## G2-SRC-GRAF-002 |
| 549 | ## G2-SRC-GRAF-003 |
| 554 | # 4.12 OpenTelemetry |
| 556 | ## G2-SRC-OTEL-001 |
| 559 | ## G2-SRC-OTEL-002 |
| 562 | ## G2-SRC-OTEL-003 |
| 565 | ## G2-SRC-OTEL-004 |
| 568 | ## G2-SRC-OTEL-005 |
| 573 | # 4.13 CI/CD |
| 575 | ## G2-SRC-CICD-001 |
| 578 | ## G2-SRC-CICD-002 |
| 582 | ## G2-SRC-CICD-003 |
| 585 | ## G2-SRC-CICD-004 |
| 590 | # 4.14 Docker / Kubernetes / Runtime Infrastructure |
| 592 | ## G2-SRC-RUNTIME-001 |
| 595 | ## G2-SRC-RUNTIME-002 |
| 598 | ## G2-SRC-RUNTIME-003 |
| 603 | # 4.15 SBOM / SCA / Vulnerability |
| 605 | ## G2-SRC-SBOM-001 |
| 608 | ## G2-SRC-SBOM-002 |
| 612 | ## G2-SRC-SBOM-003 |
| 615 | ## G2-SRC-SBOM-004 |
| 621 | # 4.16 Generic Files / Intranet / Web |
| 623 | ## G2-SRC-WEB-001 |
| 626 | ## G2-SRC-WEB-002 |
| 629 | ## G2-SRC-WEB-003 |
| 632 | ## G2-SRC-WEB-004 |
| 635 | ## G2-SRC-WEB-005 |
| 640 | # 5. Baseline, Incremental Synchronization & Reconciliation |
| 642 | ## G2-SYNC-001 — Baseline state |
| 645 | ## G2-SYNC-002 — Baseline snapshot |
| 655 | ## G2-SYNC-003 — Delta processing |
| 658 | ## G2-SYNC-004 — Delete/retire |
| 661 | ## G2-SYNC-005 — Missed-event recovery |
| 664 | ## G2-SYNC-006 — Duplicate-event handling |
| 667 | ## G2-SYNC-007 — Late event handling |
| 670 | ## G2-SYNC-008 — Dependency-aware update |
| 673 | ## G2-SYNC-009 — Consistency watermark |
| 676 | ## G2-SYNC-010 — Full rebuild is exceptional |
| 679 | ## G2-SYNC-011 — Rebuild equivalence test |
| 682 | ## G2-SYNC-012 — Connector pause/resume |
| 685 | ## G2-SYNC-013 — Backfill |
| 688 | ## G2-SYNC-014 — Selective rescan |
| 699 | # 6. Graph Evolution Engine |
| 703 | ## G2-EVOL-001 |
| 706 | ## G2-EVOL-002 |
| 711 | ## G2-EVOL-003 |
| 714 | ## G2-EVOL-004 |
| 717 | ## G2-EVOL-005 |
| 720 | ## G2-EVOL-006 |
| 723 | ## G2-EVOL-007 |
| 726 | ## G2-EVOL-008 |
| 736 | ## G2-EVOL-009 |
| 743 | ## G2-EVOL-010 |
| 746 | ## G2-EVOL-011 |
| 749 | ## G2-EVOL-012 |
| 752 | ## G2-EVOL-013 |
| 755 | ## G2-EVOL-014 |
| 758 | ## G2-EVOL-015 |
| 761 | ## G2-EVOL-016 |
| 771 | # 7. Semantic Change Journal |
| 773 | ## G2-JOURNAL-001 |
| 776 | ## G2-JOURNAL-002 |
| 789 | ## G2-JOURNAL-003 |
| 797 | ## G2-JOURNAL-004 |
| 800 | ## G2-JOURNAL-005 |
| 803 | ## G2-JOURNAL-006 |
| 808 | # 8. Semantic Event Bus |
| 812 | ## Event types |
| 830 | ## Requirements |
| 832 | ### G2-EVENT-001 |
| 835 | ### G2-EVENT-002 |
| 838 | ### G2-EVENT-003 |
| 841 | ### G2-EVENT-004 |
| 844 | ### G2-EVENT-005 |
| 855 | ### G2-EVENT-006 |
| 858 | ### G2-EVENT-007 |
| 863 | # 9. Additional Graph Domains |
| 865 | # 9.1 API & Contract Graph |
| 867 | ## G2-GRAPH-API-001 |
| 870 | ## G2-GRAPH-API-002 |
| 879 | ## G2-GRAPH-API-003 |
| 884 | # 9.2 Observability Graph |
| 886 | ## G2-GRAPH-OBS-001 |
| 899 | ## G2-GRAPH-OBS-002 |
| 902 | ## G2-GRAPH-OBS-003 |
| 907 | # 9.3 Runtime Topology Graph |
| 909 | ## G2-GRAPH-RUNTIME-001 |
| 912 | ## G2-GRAPH-RUNTIME-002 |
| 915 | ## G2-GRAPH-RUNTIME-003 |
| 920 | # 9.4 Security & Supply-Chain Graph |
| 922 | ## G2-GRAPH-SEC-001 |
| 925 | ## G2-GRAPH-SEC-002 |
| 928 | ## G2-GRAPH-SEC-003 |
| 933 | # 9.5 Test Intelligence Graph |
| 935 | ## G2-GRAPH-TEST-001 |
| 939 | ## G2-GRAPH-TEST-002 |
| 942 | ## G2-GRAPH-TEST-003 |
| 947 | # 9.6 Decision Graph |
| 949 | ## G2-GRAPH-DEC-001 |
| 961 | ## G2-GRAPH-DEC-002 |
| 964 | ## G2-GRAPH-DEC-003 |
| 969 | # 9.7 Process Graph |
| 971 | ## G2-GRAPH-PROC-001 |
| 974 | ## G2-GRAPH-PROC-002 |
| 977 | ## G2-GRAPH-PROC-003 |
| 982 | # 9.8 Business Intent / Capability Graph |
| 984 | ## G2-GRAPH-BIZ-001 |
| 994 | ## G2-GRAPH-BIZ-002 |
| 997 | ## G2-GRAPH-BIZ-003 |
| 1003 | # 10. Live Enterprise Digital Knowledge Twin |
| 1005 | ## G2-TWIN-001 |
| 1008 | ## G2-TWIN-002 |
| 1025 | ## G2-TWIN-003 |
| 1028 | ## G2-TWIN-004 |
| 1031 | ## G2-TWIN-005 |
| 1040 | # 11. Enterprise Time Machine |
| 1042 | ## G2-TIME-001 |
| 1045 | ## G2-TIME-002 |
| 1048 | ## G2-TIME-003 |
| 1051 | ## G2-TIME-004 |
| 1054 | ## G2-TIME-005 |
| 1057 | ## G2-TIME-006 |
| 1060 | ## G2-TIME-007 |
| 1065 | # 12. Counterfactual Enterprise Twin / What-If Simulation |
| 1067 | ## G2-SIM-001 |
| 1070 | ## G2-SIM-002 |
| 1073 | ## G2-SIM-003 |
| 1083 | ## G2-SIM-004 |
| 1091 | ## G2-SIM-005 |
| 1094 | ## G2-SIM-006 |
| 1097 | ## G2-SIM-007 |
| 1105 | # 13. Architecture Conformance & Semantic Architecture Compiler |
| 1107 | ## G2-ARCHC-001 |
| 1113 | ## G2-ARCHC-002 |
| 1116 | ## G2-ARCHC-003 |
| 1123 | ## G2-ARCHC-004 |
| 1126 | ## G2-ARCHC-005 |
| 1129 | ## G2-ARCHC-006 |
| 1132 | ## G2-ARCHC-007 |
| 1135 | ## G2-ARCHC-008 |
| 1138 | ## G2-ARCHC-009 |
| 1143 | # 14. Causal Intelligence |
| 1147 | ## G2-CAUSE-001 |
| 1150 | ## G2-CAUSE-002 |
| 1157 | ## G2-CAUSE-003 |
| 1160 | ## G2-CAUSE-004 |
| 1168 | ## G2-CAUSE-005 |
| 1171 | ## G2-CAUSE-006 |
| 1176 | # 15. Enterprise Knowledge Immune System |
| 1180 | ## G2-IMMUNE-001 |
| 1183 | ## G2-IMMUNE-002 |
| 1186 | ## G2-IMMUNE-003 |
| 1189 | ## G2-IMMUNE-004 |
| 1192 | ## G2-IMMUNE-005 |
| 1195 | ## G2-IMMUNE-006 |
| 1198 | ## G2-IMMUNE-007 |
| 1201 | ## G2-IMMUNE-008 |
| 1204 | ## G2-IMMUNE-009 |
| 1207 | ## G2-IMMUNE-010 |
| 1210 | ## G2-IMMUNE-011 |
| 1213 | ## G2-IMMUNE-012 |
| 1216 | ## G2-IMMUNE-013 |
| 1221 | # 16. Controlled Ontology Evolution |
| 1223 | ## G2-OEVO-001 |
| 1226 | ## G2-OEVO-002 |
| 1229 | ## G2-OEVO-003 |
| 1238 | ## G2-OEVO-004 |
| 1241 | ## G2-OEVO-005 |
| 1244 | ## G2-OEVO-006 |
| 1249 | # 17. Process Mining |
| 1251 | ## G2-PM-001 |
| 1254 | ## G2-PM-002 |
| 1257 | ## G2-PM-003 |
| 1266 | ## G2-PM-004 |
| 1269 | ## G2-PM-005 |
| 1274 | # 18. Knowledge Capsules |
| 1278 | ## G2-CAP-001 |
| 1289 | ## G2-CAP-002 |
| 1292 | ## G2-CAP-003 |
| 1295 | ## G2-CAP-004 |
| 1298 | ## G2-CAP-005 |
| 1308 | ## G2-CAP-006 |
| 1313 | # 19. Native Semantic Query Operators |
| 1317 | ## G2-QOP-001 — WHY |
| 1320 | ## G2-QOP-002 — WHY NOT |
| 1323 | ## G2-QOP-003 — WHAT IF |
| 1326 | ## G2-QOP-004 — WHAT CHANGED |
| 1329 | ## G2-QOP-005 — WHEN |
| 1332 | ## G2-QOP-006 — WHO |
| 1335 | ## G2-QOP-007 — WHERE |
| 1338 | ## G2-QOP-008 — HOW |
| 1341 | ## G2-QOP-009 |
| 1346 | # 20. Intent-to-Runtime Traceability |
| 1348 | ## G2-I2R-001 |
| 1352 | ## G2-I2R-002 |
| 1355 | ## G2-I2R-003 |
| 1358 | ## G2-I2R-004 |
| 1361 | ## G2-I2R-005 |
| 1366 | # 21. Knowledge Debt |
| 1368 | ## G2-KD-001 |
| 1371 | ## G2-KD-002 |
| 1386 | ## G2-KD-003 |
| 1395 | ## G2-KD-004 |
| 1398 | ## G2-KD-005 |
| 1401 | ## G2-KD-006 |
| 1406 | # 22. Knowledge Reliability SLOs |
| 1408 | ## G2-SLO-001 |
| 1418 | ## G2-SLO-002 |
| 1421 | ## G2-SLO-003 |
| 1424 | ## G2-SLO-004 |
| 1427 | ## G2-SLO-005 |
| 1432 | # 23. Next-Generation GUI / Application Requirements |
| 1436 | ## 23.1 Lens framework |
| 1438 | ### G2-UX-LENS-001 |
| 1441 | ### Required lenses |
| 1464 | ### G2-UX-LENS-002 |
| 1467 | ### G2-UX-LENS-003 |
| 1472 | # 24. Advanced Graph Canvas |
| 1474 | ## G2-UX-GRAPH-001 |
| 1477 | ## G2-UX-GRAPH-002 |
| 1480 | ## G2-UX-GRAPH-003 |
| 1483 | ## G2-UX-GRAPH-004 |
| 1486 | ## G2-UX-GRAPH-005 |
| 1489 | ## G2-UX-GRAPH-006 |
| 1492 | ## G2-UX-GRAPH-007 |
| 1495 | ## G2-UX-GRAPH-008 |
| 1498 | ## G2-UX-GRAPH-009 |
| 1501 | ## G2-UX-GRAPH-010 |
| 1504 | ## G2-UX-GRAPH-011 |
| 1507 | ## G2-UX-GRAPH-012 |
| 1510 | ## G2-UX-GRAPH-013 |
| 1513 | ## G2-UX-GRAPH-014 |
| 1516 | ## G2-UX-GRAPH-015 |
| 1519 | ## G2-UX-GRAPH-016 |
| 1524 | # 25. Graph Playback |
| 1526 | ## G2-UX-PLAY-001 |
| 1529 | ## G2-UX-PLAY-002 |
| 1538 | ## G2-UX-PLAY-003 |
| 1541 | ## G2-UX-PLAY-004 |
| 1544 | ## G2-UX-PLAY-005 |
| 1549 | # 26. Admin / Engineering GUI Additions |
| 1551 | ## G2-ADMIN-001 |
| 1554 | ## G2-ADMIN-002 |
| 1557 | ## G2-ADMIN-003 |
| 1560 | ## G2-ADMIN-004 |
| 1563 | ## G2-ADMIN-005 |
| 1566 | ## G2-ADMIN-006 |
| 1569 | ## G2-ADMIN-007 |
| 1572 | ## G2-ADMIN-008 |
| 1575 | ## G2-ADMIN-009 |
| 1578 | ## G2-ADMIN-010 |
| 1581 | ## G2-ADMIN-011 |
| 1584 | ## G2-ADMIN-012 |
| 1587 | ## G2-ADMIN-013 |
| 1590 | ## G2-ADMIN-014 |
| 1593 | ## G2-ADMIN-015 |
| 1596 | ## G2-ADMIN-016 |
| 1599 | ## G2-ADMIN-017 |
| 1604 | # 27. VS Code Additions |
| 1606 | ## G2-VSC-001 |
| 1609 | ## G2-VSC-002 |
| 1612 | ## G2-VSC-003 |
| 1615 | ## G2-VSC-004 |
| 1618 | ## G2-VSC-005 |
| 1621 | ## G2-VSC-006 |
| 1624 | ## G2-VSC-007 |
| 1627 | ## G2-VSC-008 |
| 1632 | # 28. Telemetry Semantics and Storage Rules |
| 1634 | ## G2-TEL-001 |
| 1637 | ## G2-TEL-002 |
| 1640 | ## G2-TEL-003 |
| 1643 | ## G2-TEL-004 |
| 1646 | ## G2-TEL-005 |
| 1649 | ## G2-TEL-006 |
| 1652 | ## G2-TEL-007 |
| 1655 | ## G2-TEL-008 |
| 1660 | # 29. Security Requirements for Acquisition/Crawling |
| 1662 | ## G2-SEC-CRAWL-001 |
| 1665 | ## G2-SEC-CRAWL-002 |
| 1668 | ## G2-SEC-CRAWL-003 |
| 1671 | ## G2-SEC-CRAWL-004 |
| 1674 | ## G2-SEC-CRAWL-005 |
| 1677 | ## G2-SEC-CRAWL-006 |
| 1680 | ## G2-SEC-CRAWL-007 |
| 1683 | ## G2-SEC-CRAWL-008 |
| 1686 | ## G2-SEC-CRAWL-009 |
| 1689 | ## G2-SEC-CRAWL-010 |
| 1692 | ## G2-SEC-CRAWL-011 |
| 1695 | ## G2-SEC-CRAWL-012 |
| 1700 | # 30. Observability Requirements |
| 1702 | ## G2-OBS-001 |
| 1705 | ## G2-OBS-002 |
| 1714 | ## G2-OBS-003 |
| 1720 | ## G2-OBS-004 |
| 1723 | ## G2-OBS-005 |
| 1726 | ## G2-OBS-006 |
| 1731 | # 31. Performance & Scale Requirements |
| 1735 | ## G2-PERF-001 |
| 1738 | ## G2-PERF-002 |
| 1741 | ## G2-PERF-003 |
| 1744 | ## G2-PERF-004 |
| 1747 | ## G2-PERF-005 |
| 1750 | ## G2-PERF-006 |
| 1753 | ## G2-PERF-007 |
| 1756 | ## G2-PERF-008 |
| 1761 | # 32. Reliability & Recovery |
| 1763 | ## G2-REL-001 |
| 1766 | ## G2-REL-002 |
| 1769 | ## G2-REL-003 |
| 1772 | ## G2-REL-004 |
| 1775 | ## G2-REL-005 |
| 1778 | ## G2-REL-006 |
| 1781 | ## G2-REL-007 |
| 1784 | ## G2-REL-008 |
| 1789 | # 33. AI Agent Development Rules |
| 1814 | # 34. Required Data Contracts |
| 1842 | # 35. Required APIs / Service Operations |
| 1875 | # 36. Testing Requirements |
| 1877 | ## Connector contract tests |
| 1892 | ## Graph evolution tests |
| 1900 | ## Telemetry tests |
| 1907 | ## UI tests |
| 1915 | ## Security tests |
| 1926 | # 37. Acceptance Scenarios |
| 1928 | ## Scenario A — Baseline and incremental Jira/Git |
| 1936 | ## Scenario B — ServiceNow incident |
| 1942 | ## Scenario C — Observability |
| 1948 | ## Scenario D — Time Machine |
| 1953 | ## Scenario E — Simulation |
| 1959 | ## Scenario F — Architecture conformance |
| 1965 | ## Scenario G — Knowledge Immune System |
| 1973 | # 38. Phase Priority |
| 1975 | ## P0 — Must build early |
| 1986 | ## P1 — High-value enterprise expansion |
| 1997 | ## P2 — Differentiating intelligence |
| 2006 | ## P3 — Moonshot/advanced |
| 2016 | # 39. Definition of Done |
| 2035 | # 40. North-Star Architecture |

### EOIP-engg-doc-pkg/implementation/wp-agent-memory.md

| Property | Value |
| --- | --- |
| Lines read | 77 |
| Nonblank lines | 71 |
| SHA-256 prefix | 9f72fc15038d4cff |
| First line | # WP-AGENT-MEMORY Implementation Plan |
| Last line | **Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-MEM-001`. |
| Requirement-like lines | 42 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, FR-MEM-001, WP-AGENT-MEMORY-01, WP-AGENT-MEMORY-02, WP-AGENT-MEMORY-03, WP-AGENT-MEMORY-04, WP-AGENT-MEMORY-05, WP-AGENT-MEMORY-06 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # WP-AGENT-MEMORY Implementation Plan |
| 11 | ## Requirements |
| 22 | ## Implementation sequence |
| 24 | ### WP-AGENT-MEMORY-01 — Agent contract |
| 33 | ### WP-AGENT-MEMORY-02 — Bounded agent runtime |
| 42 | ### WP-AGENT-MEMORY-03 — TraceImpact agent |
| 51 | ### WP-AGENT-MEMORY-04 — Write/action approval boundary |
| 60 | ### WP-AGENT-MEMORY-05 — Controlled self-modification |
| 69 | ### WP-AGENT-MEMORY-06 — Scoped memory records |

### EOIP-engg-doc-pkg/implementation/wp-codegraph.md

| Property | Value |
| --- | --- |
| Lines read | 67 |
| Nonblank lines | 61 |
| SHA-256 prefix | 69f1742ee7be7eec |
| First line | # WP-CODEGRAPH Implementation Plan |
| Last line | **Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-CODE-005`. |
| Requirement-like lines | 24 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-CODE-001, FR-CODE-002, FR-CODE-003, FR-CODE-004, FR-CODE-005, WP-CODEGRAPH-01, WP-CODEGRAPH-02, WP-CODEGRAPH-03, WP-CODEGRAPH-04, WP-CODEGRAPH-05 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # WP-CODEGRAPH Implementation Plan |
| 11 | ## Requirements |
| 21 | ## Implementation sequence |
| 23 | ### WP-CODEGRAPH-01 — Deterministic code parser |
| 32 | ### WP-CODEGRAPH-02 — Python and TypeScript MVP parsing |
| 41 | ### WP-CODEGRAPH-03 — Commit-to-symbol linking |
| 50 | ### WP-CODEGRAPH-04 — Call/import/dependency edges |
| 59 | ### WP-CODEGRAPH-05 — Source navigation |

### EOIP-engg-doc-pkg/implementation/wp-connectors.md

| Property | Value |
| --- | --- |
| Lines read | 107 |
| Nonblank lines | 101 |
| SHA-256 prefix | d088338c0da4e9e6 |
| First line | # WP-CONNECTORS Implementation Plan |
| Last line | **Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-SNOW-001`. |
| Requirement-like lines | 59 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen | FR-CONF-001, FR-CONN-001, FR-CONN-002, FR-CONN-003, FR-CONN-004, FR-CONN-005, FR-CONN-006, FR-CONN-007, FR-SNOW-001, WP-CONNECTORS-01, WP-CONNECTORS-02, WP-CONNECTORS-03, WP-CONNECTORS-04, WP-CONNECTORS-05, WP-CONNECTORS-06, WP-CONNECTORS-07, WP-CONNECTORS-08, WP-CONNECTORS-09 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # WP-CONNECTORS Implementation Plan |
| 11 | ## Requirements |
| 25 | ## Implementation sequence |
| 27 | ### WP-CONNECTORS-01 — Connector SDK |
| 36 | ### WP-CONNECTORS-02 — Jira JSON connector |
| 45 | ### WP-CONNECTORS-03 — Git repository connector |
| 54 | ### WP-CONNECTORS-04 — GitLab metadata adapter |
| 63 | ### WP-CONNECTORS-05 — Connector resiliency |
| 72 | ### WP-CONNECTORS-06 — Dry run and replay |
| 81 | ### WP-CONNECTORS-07 — Source deletion semantics |
| 90 | ### WP-CONNECTORS-08 — Confluence connector |
| 99 | ### WP-CONNECTORS-09 — ServiceNow connector |

### EOIP-engg-doc-pkg/implementation/wp-experience.md

| Property | Value |
| --- | --- |
| Lines read | 77 |
| Nonblank lines | 71 |
| SHA-256 prefix | 7387b1b6dbce48a2 |
| First line | # WP-EXPERIENCE Implementation Plan |
| Last line | **Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-VSCODE-002`. |
| Requirement-like lines | 44 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen | FR-ADMIN-001, FR-ADMIN-002, FR-UI-001, FR-UI-002, FR-VSCODE-001, FR-VSCODE-002, WP-EXPERIENCE-01, WP-EXPERIENCE-02, WP-EXPERIENCE-03, WP-EXPERIENCE-04, WP-EXPERIENCE-05, WP-EXPERIENCE-06 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # WP-EXPERIENCE Implementation Plan |
| 11 | ## Requirements |
| 22 | ## Implementation sequence |
| 24 | ### WP-EXPERIENCE-01 — User web application |
| 33 | ### WP-EXPERIENCE-02 — Graph explorer |
| 42 | ### WP-EXPERIENCE-03 — Admin ingestion UI |
| 51 | ### WP-EXPERIENCE-04 — Admin graph quality UI |
| 60 | ### WP-EXPERIENCE-05 — VS Code context extension |
| 69 | ### WP-EXPERIENCE-06 — VS Code trace/impact commands |

### EOIP-engg-doc-pkg/implementation/wp-foundation.md

| Property | Value |
| --- | --- |
| Lines read | 67 |
| Nonblank lines | 61 |
| SHA-256 prefix | f3e58f7181d30a75 |
| First line | # WP-FOUNDATION Implementation Plan |
| Last line | **Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `NFR-MAINT-001`. |
| Requirement-like lines | 30 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen | FR-GRAPH-001, FR-GRAPH-002, FR-GRAPH-003, FR-GRAPH-004, NFR-MAINT-001, WP-FOUNDATION-01, WP-FOUNDATION-02, WP-FOUNDATION-03, WP-FOUNDATION-04, WP-FOUNDATION-05 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # WP-FOUNDATION Implementation Plan |
| 11 | ## Requirements |
| 21 | ## Implementation sequence |
| 23 | ### WP-FOUNDATION-01 — HugeGraph authoritative store |
| 32 | ### WP-FOUNDATION-02 — Logical graph domains |
| 41 | ### WP-FOUNDATION-03 — Schema bootstrap |
| 50 | ### WP-FOUNDATION-04 — Canonical identifiers |
| 59 | ### WP-FOUNDATION-05 — Modular monolith boundary |

### EOIP-engg-doc-pkg/implementation/wp-ingestion.md

| Property | Value |
| --- | --- |
| Lines read | 67 |
| Nonblank lines | 61 |
| SHA-256 prefix | 32732c84523978b4 |
| First line | # WP-INGESTION Implementation Plan |
| Last line | **Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-INGEST-005`. |
| Requirement-like lines | 32 |
| Status/gap/risk-like lines | 1 |
| Requirement IDs seen | FR-INGEST-001, FR-INGEST-002, FR-INGEST-003, FR-INGEST-004, FR-INGEST-005, WP-INGESTION-01, WP-INGESTION-02, WP-INGESTION-03, WP-INGESTION-04, WP-INGESTION-05 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # WP-INGESTION Implementation Plan |
| 11 | ## Requirements |
| 21 | ## Implementation sequence |
| 23 | ### WP-INGESTION-01 — Raw capture |
| 32 | ### WP-INGESTION-02 — Canonicalization |
| 41 | ### WP-INGESTION-03 — Idempotent mutation |
| 50 | ### WP-INGESTION-04 — Ingestion job lifecycle |
| 59 | ### WP-INGESTION-05 — Dead-letter processing |

### EOIP-engg-doc-pkg/implementation/wp-mcp.md

| Property | Value |
| --- | --- |
| Lines read | 37 |
| Nonblank lines | 31 |
| SHA-256 prefix | 8c7ee26a187fc1be |
| First line | # WP-MCP Implementation Plan |
| Last line | **Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-MCP-002`. |
| Requirement-like lines | 20 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen | FR-MCP-001, FR-MCP-002, WP-MCP-01, WP-MCP-02 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # WP-MCP Implementation Plan |
| 11 | ## Requirements |
| 18 | ## Implementation sequence |
| 20 | ### WP-MCP-01 — MCP read server |
| 29 | ### WP-MCP-02 — MCP action separation |

### EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md

| Property | Value |
| --- | --- |
| Lines read | 137 |
| Nonblank lines | 131 |
| SHA-256 prefix | 05ccb1b4a514712c |
| First line | # WP-ONTOLOGY-GRAPH Implementation Plan |
| Last line | **Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-TEMP-001`. |
| Requirement-like lines | 79 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | FR-GRAPH-005, FR-GRAPH-006, FR-GRAPH-008, FR-GRAPH-009, FR-GRAPH-010, FR-ID-001, FR-ID-002, FR-ONTO-001, FR-ONTO-002, FR-PROV-001, FR-PROV-002, FR-TEMP-001, WP-ONTOLOGY-GRAPH-01, WP-ONTOLOGY-GRAPH-02, WP-ONTOLOGY-GRAPH-03, WP-ONTOLOGY-GRAPH-04, WP-ONTOLOGY-GRAPH-05, WP-ONTOLOGY-GRAPH-06, WP-ONTOLOGY-GRAPH-07, WP-ONTOLOGY-GRAPH-08, WP-ONTOLOGY-GRAPH-09, WP-ONTOLOGY-GRAPH-10, WP-ONTOLOGY-GRAPH-11, WP-ONTOLOGY-GRAPH-12 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # WP-ONTOLOGY-GRAPH Implementation Plan |
| 11 | ## Requirements |
| 28 | ## Implementation sequence |
| 30 | ### WP-ONTOLOGY-GRAPH-01 — Meta graph |
| 39 | ### WP-ONTOLOGY-GRAPH-02 — Cross-domain bridge edges |
| 48 | ### WP-ONTOLOGY-GRAPH-03 — Index strategy |
| 57 | ### WP-ONTOLOGY-GRAPH-04 — Graph version journal |
| 66 | ### WP-ONTOLOGY-GRAPH-05 — RDF/OWL interoperability |
| 75 | ### WP-ONTOLOGY-GRAPH-06 — Enterprise ontology vocabulary |
| 84 | ### WP-ONTOLOGY-GRAPH-07 — Relationship semantics |
| 93 | ### WP-ONTOLOGY-GRAPH-08 — Evidence model |
| 102 | ### WP-ONTOLOGY-GRAPH-09 — Provenance traversal |
| 111 | ### WP-ONTOLOGY-GRAPH-10 — Deterministic identity resolution |
| 120 | ### WP-ONTOLOGY-GRAPH-11 — Ambiguous identity candidates |
| 129 | ### WP-ONTOLOGY-GRAPH-12 — Bitemporal-ready fields |

### EOIP-engg-doc-pkg/implementation/wp-query.md

| Property | Value |
| --- | --- |
| Lines read | 107 |
| Nonblank lines | 101 |
| SHA-256 prefix | 16ead715beffd155 |
| First line | # WP-QUERY Implementation Plan |
| Last line | **Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-GRAPH-007`. |
| Requirement-like lines | 46 |
| Status/gap/risk-like lines | 1 |
| Requirement IDs seen | FR-GRAPH-007, FR-QUERY-001, FR-QUERY-002, FR-QUERY-003, FR-QUERY-004, FR-QUERY-005, FR-QUERY-006, FR-QUERY-007, FR-QUERY-008, WP-QUERY-01, WP-QUERY-02, WP-QUERY-03, WP-QUERY-04, WP-QUERY-05, WP-QUERY-06, WP-QUERY-07, WP-QUERY-08, WP-QUERY-09 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # WP-QUERY Implementation Plan |
| 11 | ## Requirements |
| 25 | ## Implementation sequence |
| 27 | ### WP-QUERY-01 — Structured QueryPlan |
| 36 | ### WP-QUERY-02 — Path query |
| 45 | ### WP-QUERY-03 — Impact analysis |
| 54 | ### WP-QUERY-04 — Entity search |
| 63 | ### WP-QUERY-05 — Natural-language query interpretation |
| 72 | ### WP-QUERY-06 — Query safety policy |
| 81 | ### WP-QUERY-07 — Query evidence envelope |
| 90 | ### WP-QUERY-08 — Raw Gremlin admin boundary |
| 99 | ### WP-QUERY-09 — Gremlin repository |

### EOIP-engg-doc-pkg/implementation/wp-rag.md

| Property | Value |
| --- | --- |
| Lines read | 77 |
| Nonblank lines | 71 |
| SHA-256 prefix | 3d55d1cac4ad980d |
| First line | # WP-RAG Implementation Plan |
| Last line | **Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-RAG-006`. |
| Requirement-like lines | 45 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen | FR-RAG-001, FR-RAG-002, FR-RAG-003, FR-RAG-004, FR-RAG-005, FR-RAG-006, WP-RAG-01, WP-RAG-02, WP-RAG-03, WP-RAG-04, WP-RAG-05, WP-RAG-06 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # WP-RAG Implementation Plan |
| 11 | ## Requirements |
| 22 | ## Implementation sequence |
| 24 | ### WP-RAG-01 — Retrieval router |
| 33 | ### WP-RAG-02 — GraphRAG evidence retrieval |
| 42 | ### WP-RAG-03 — Local model abstraction |
| 51 | ### WP-RAG-04 — No mandatory vector DB in MVP |
| 60 | ### WP-RAG-05 — RAG evaluation harness |
| 69 | ### WP-RAG-06 — Adaptive RAG strategy framework |

### EOIP-engg-doc-pkg/implementation/wp-security-ops.md

| Property | Value |
| --- | --- |
| Lines read | 157 |
| Nonblank lines | 151 |
| SHA-256 prefix | 2ddae9a952d1bd7c |
| First line | # WP-SECURITY-OPS Implementation Plan |
| Last line | **Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `NFR-PRIV-001`. |
| Requirement-like lines | 96 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen | NFR-MAINT-001, NFR-OPS-001, NFR-OPS-002, NFR-PERF-001, NFR-PRIV-001, NFR-REL-001, NFR-REL-002, NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-005, NFR-SEC-006, NFR-SEC-007, WP-SECURITY-OPS-01, WP-SECURITY-OPS-02, WP-SECURITY-OPS-03, WP-SECURITY-OPS-04, WP-SECURITY-OPS-05, WP-SECURITY-OPS-06, WP-SECURITY-OPS-07, WP-SECURITY-OPS-08, WP-SECURITY-OPS-09, WP-SECURITY-OPS-10, WP-SECURITY-OPS-11, WP-SECURITY-OPS-12, WP-SECURITY-OPS-13, WP-SECURITY-OPS-14 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # WP-SECURITY-OPS Implementation Plan |
| 11 | ## Requirements |
| 30 | ## Implementation sequence |
| 32 | ### WP-SECURITY-OPS-01 — No outbound enterprise-data egress |
| 41 | ### WP-SECURITY-OPS-02 — Secret isolation |
| 50 | ### WP-SECURITY-OPS-03 — Input/file safety |
| 59 | ### WP-SECURITY-OPS-04 — Prompt/tool injection defenses |
| 68 | ### WP-SECURITY-OPS-05 — Authentication without MVP RBAC |
| 77 | ### WP-SECURITY-OPS-06 — Container hardening |
| 86 | ### WP-SECURITY-OPS-07 — Audit events |
| 95 | ### WP-SECURITY-OPS-08 — Restart-safe processing |
| 104 | ### WP-SECURITY-OPS-09 — Backup and restore |
| 113 | ### WP-SECURITY-OPS-10 — Structured logging and health |
| 122 | ### WP-SECURITY-OPS-11 — Local metrics |
| 131 | ### WP-SECURITY-OPS-12 — Benchmark-defined objectives |
| 140 | ### WP-SECURITY-OPS-13 — Modular monolith boundary |
| 149 | ### WP-SECURITY-OPS-14 — Data minimization and classification |

### EOIP-engg-doc-pkg/implementation/wp-validation.md

| Property | Value |
| --- | --- |
| Lines read | 47 |
| Nonblank lines | 41 |
| SHA-256 prefix | ed959d83ce6d3163 |
| First line | # WP-VALIDATION Implementation Plan |
| Last line | **Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-VALID-003`. |
| Requirement-like lines | 21 |
| Status/gap/risk-like lines | 1 |
| Requirement IDs seen | FR-VALID-001, FR-VALID-002, FR-VALID-003, WP-VALIDATION-01, WP-VALIDATION-02, WP-VALIDATION-03 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # WP-VALIDATION Implementation Plan |
| 11 | ## Requirements |
| 19 | ## Implementation sequence |
| 21 | ### WP-VALIDATION-01 — Graph validation rules |
| 30 | ### WP-VALIDATION-02 — Validation gates |
| 39 | ### WP-VALIDATION-03 — Graph quality metrics |

### EOIP-engg-doc-pkg/KGR-implementation-plan.md

| Property | Value |
| --- | --- |
| Lines read | 2838 |
| Nonblank lines | 2337 |
| SHA-256 prefix | 863c5bac10c21f2d |
| First line | # KGR — Knowledge Graph Renderer: Phase-by-Phase Implementation Plan |
| Last line | 17. **UX pattern research**: Search-to-explore (Linkurious), progressive disclosure, undo/redo exploration, collaborative annotations, NL graph queries, AI-assisted exploration, dashboard integration |
| Requirement-like lines | 409 |
| Status/gap/risk-like lines | 72 |
| Requirement IDs seen | FR-KGR-010, FR-KGR-011, FR-KGR-012, FR-KGR-013, FR-KGR-014, FR-KGR-015, FR-KGR-016 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # KGR — Knowledge Graph Renderer: Phase-by-Phase Implementation Plan |
| 10 | ## Architecture Overview |
| 12 | ### Rendering Strategy |
| 19 | ### Why This Stack Beats Every Competitor |
| 30 | ### Component Architecture |
| 93 | ### Backend API — Full Endpoint Inventory |
| 96 | # DONE (Phase 1) |
| 103 | # Phase 3 — Advanced Centrality |
| 106 | # Phase 4 — Community & Paths |
| 110 | # Phase 5 — Similarity & Prediction |
| 114 | # Phase 6 — Structure Analysis |
| 119 | # Phase 7 — Real-Time |
| 123 | # Phase 8 — Advanced Analytics |
| 129 | ### Request/Response Contracts for All Endpoints |
| 132 | # --- DONE --- |
| 137 | # Response: {target_id, total_affected, by_depth: {1: N, 2: M}, by_type: {"File": N}, risk: "HIGH"\|"MEDIUM"\|"LOW", affected_ids: [...]} |
| 141 | # Response: {canonical_id: {canonical_id, degree, in_degree, out_degree, betweenness, closeness, page_rank}} |
| 143 | # --- PLANNED --- |
| 148 | # Response: {canonical_id: {degree, in_degree, out_degree, betweenness, closeness, page_rank, eigenvector, katz, hits_hub, hits_authority}} |
| 154 | # Response: {communities: [{id: int, members: [canonical_id], size: int, label_distribution: {}}], modularity: float, algorithm: str} |
| 161 | # Response: {paths: [[canonical_id, ...]], count: int} |
| 167 | # Response: [{canonical_id, score: float, common_neighbors: [canonical_id]}] |
| 173 | # Response: [{source_id, target_id, score: float, algorithm: str}] |
| 177 | # Response: {cores: [{k: int, members: [canonical_id], size: int}], max_k: int} |
| 182 | # Response: {broken_paths: int, orphaned_entities: int, affected_components: int, centrality_changes: {canonical_id: {before, after}}} |
| 187 | # Response: {added_nodes: [...], removed_nodes: [...], modified_nodes: [...], added_edges: [...], removed_edges: [...], structural_changes: {broken_paths: int, new_components: int}} |
| 192 | # Response: [{canonical_id, anomaly_type: str, score: float, explanation: str}] |
| 197 | ## Implementation Status |
| 217 | ## Phase 1: Foundation — COMPLETE |
| 222 | ### What Was Built |
| 230 | ### Key Implementation Details |
| 238 | ## Phase 2: Component Extraction & New Graph Types |
| 242 | ### 2.1 Extract Components from KGRExplorer.jsx (3 days) |
| 273 | ### 2.2 Impact/Dependency Graph View (2 days) |
| 285 | ### 2.3 Similarity/Cluster Graph View (2 days) |
| 297 | ### 2.4 Edge Inspector Component (1 day) |
| 309 | ### 2.5 Update KGRExplorer.jsx (1 day) |
| 317 | ### Tests (Phase 2) |
| 332 | ## Phase 3: Full Centrality Suite & Client-Side Algorithms |
| 336 | ### 3.1 Backend: Full Centrality Engine (3 days) |
| 344 | # Build adjacency lists once, compute all requested algorithms |
| 348 | # For each node s: BFS from s, accumulate pair dependencies |
| 352 | # BFS from each node, sum distances, invert |
| 356 | # Initialize uniform, iterate: PR(v) = (1-d)/N + d * sum(PR(u)/out(u)) |
| 360 | # Initialize uniform, iterate: x_new = A * x_old, normalize |
| 364 | # x = beta * (I - alpha*A)^-1 * 1 — approximated via power iteration |
| 368 | # Initialize uniform, iterate: auth = A^T * hub, hub = A * auth, normalize |
| 378 | ### 3.2 Client-Side Graph Algorithms (3 days) |
| 408 | ### 3.3 Centrality Radar Chart (2 days) |
| 420 | ### 3.4 Inspector Impact Tab Enhancement (2 days) |
| 433 | ### 3.5 Path Finding (2 days) |
| 449 | ### Tests (Phase 3) |
| 465 | ## Phase 4: Community Detection, Filtering & Keyboard Navigation |
| 469 | ### 4.1 Backend: Community Detection Engine (3 days) |
| 499 | ### 4.2 Client-Side Community Detection (2 days) |
| 519 | ### 4.3 10-Dimensional Filter Bar (3 days) |
| 560 | ### 4.4 Keyboard Navigation (2 days) |
| 585 | ### 4.5 Context Menu (2 days) |
| 614 | ### 4.6 Exploration History (1 day) |
| 625 | ### 4.7 Bookmarks (1 day) |
| 635 | ### Tests (Phase 4) |
| 653 | ## Phase 5: Timeline, Export Suite, Annotations & Visual Polish |
| 657 | ### 5.1 Timeline Scrubber (3 days) |
| 670 | ### 5.2 Export Suite (3 days) |
| 692 | ### 5.3 Annotation System (2 days) |
| 704 | ### 5.4 Semantic Zoom Enhancement (2 days) |
| 719 | ### 5.5 Fisheye Distortion (1 day) |
| 729 | ### 5.6 Edge Bundling (1 day) |
| 739 | ### 5.7 Color-Blind Safe Palette (1 day) |
| 751 | ### 5.8 Similarity Analysis (2 days) |
| 771 | ### Tests (Phase 5) |
| 789 | ## Phase 6: Large-Graph Rendering & Performance |
| 793 | ### 6.1 Sigma.js Integration (3 days) |
| 827 | ### 6.2 Web Worker Layout Engine (2 days) |
| 859 | ### 6.3 Progressive Rendering (2 days) |
| 878 | ### 6.4 Virtual Scrolling Entity Strip (1 day) |
| 886 | ### 6.5 Backend: Structure Analysis Endpoints (2 days) |
| 892 | # Iteratively remove nodes with degree < k |
| 903 | ### Tests (Phase 6) |
| 918 | ## Phase 7: Real-Time Updates & WebSocket Integration |
| 922 | ### 7.1 WebSocket Event Service (2 days) |
| 926 | # packages/eoip/events/emitter.py |
| 973 | # Return events since timestamp from in-memory ring buffer (last 1000 events) |
| 976 | ### 7.2 Client-Side WebSocket Manager (2 days) |
| 1012 | ### 7.3 Event Feed Panel (1 day) |
| 1024 | ### Tests (Phase 7) |
| 1037 | ## Phase 8: Graph Comparison, What-If & Advanced Analytics |
| 1041 | ### 8.1 Backend: What-If Engine (2 days) |
| 1054 | # 1. Find all edges connected to this entity |
| 1055 | # 2. For each neighbor: check if removing these edges disconnects it |
| 1056 | # 3. Count broken shortest paths through this entity |
| 1057 | # 4. Recompute centrality for affected neighbors |
| 1058 | # 5. Return impact summary |
| 1066 | ### 8.2 Backend: Anomaly Detection (2 days) |
| 1083 | ### 8.3 Graph Diff View (3 days) |
| 1111 | ### 8.4 What-If Simulation UI (2 days) |
| 1125 | ### 8.5 Graph Health Dashboard (2 days) |
| 1143 | ### Tests (Phase 8) |
| 1161 | ## Phase 9: Component Wiring & Integration |
| 1165 | ### 9.1 Wire useGraphEvents Hook into KGRExplorer (0.5 day) |
| 1175 | ### 9.2 Wire LayoutWorker.js into Renderers (0.5 day) |
| 1185 | ### 9.3 Wire GraphToolbar into KGRExplorer (0.5 day) |
| 1195 | ### 9.4 Wire ExportMenu into KGRExplorer (0.5 day) |
| 1206 | ### 9.5 Wire TimelineScrubber into Temporal View (0.5 day) |
| 1216 | ### 9.6 Populate Community Filter Dropdown (0.5 day) |
| 1226 | ### 9.7 Connect Minimap Viewport Rectangle (0.5 day) |
| 1236 | ### 9.8 Implement Side-by-Side Diff View (0.5 day) |
| 1248 | ### 9.9 Wire Annotation Inclusion in Exports (0.5 day) |
| 1258 | ### 9.10 Deduplicate Inline vs Standalone Components (1 day) |
| 1276 | ### Tests (Phase 9) |
| 1291 | ## Phase 10: Advanced Competitor Features |
| 1295 | ### 10.1 Node Group Collapsing & Combo Declutter (3 days) |
| 1326 | ### 10.2 Code + Graph Side-by-Side View (3 days) |
| 1336 | # Read file from configured repository path |
| 1337 | # Return: {content: str, language: str, line_count: int} |
| 1362 | ### 10.3 Four New Export Formats (2 days) |
| 1400 | ### 10.4 Visual Query Builder (3 days) |
| 1431 | ### 10.5 Dead Code & Orphaned Entity Detection (2 days) |
| 1438 | # Add to AnomalyDetector |
| 1452 | # Returns: [{canonical_id, label, name, in_degree: 0, last_ingestion_run}] |
| 1461 | ### 10.6 Community Auto-Labeling (1 day) |
| 1468 | # Add to CommunityDetectionEngine |
| 1492 | ### 10.7 Geo-Mode (2 days) |
| 1517 | ### 10.8 PR / Change Impact Dashboard (2 days) |
| 1527 | # 1. Fetch open MRs from GitLab connector (or PRs from GitHub) |
| 1528 | # 2. For each MR: find Commit vertices, trace to modified entities |
| 1529 | # 3. Map modified entities to communities (from last community detection run) |
| 1530 | # 4. Compute pairwise overlap between MRs |
| 1531 | # 5. Return: [{mr_id, title, author, communities_touched: [], entities_modified: int}] |
| 1532 | # 6. conflicts: [{mr_a, mr_b, overlap_communities: [], overlap_pct: float, risk: "HIGH"\|"MEDIUM"\|"LOW"}] |
| 1551 | ### 10.9 AMBIGUOUS Evidence Status Support (0.5 day) |
| 1565 | ### Tests (Phase 10) |
| 1590 | ## Cross-Cutting Concerns (Applied Across All Phases) |
| 1592 | ### CSS Design System Extension |
| 1619 | ### Testing Strategy |
| 1628 | ### Dependencies |
| 1631 | # Python (already in requirements or to add) |
| 1632 | # No new Python dependencies — all algorithms implemented from scratch |
| 1633 | # This avoids the dependency bloat that plagues Graphistry, yFiles, Neo4j |
| 1635 | # JavaScript (via CDN or bundled) |
| 1648 | ## Phase Summary |
| 1664 | ### Definition of Done (per phase) |
| 1676 | ### Dependencies Between Phases |
| 1704 | ## Phase 11: Visual Intelligence & Polish |
| 1708 | ### 11.1 Semantic Zoom (3 Levels) (2 days) |
| 1741 | ### 11.2 Fisheye Distortion (2 days) |
| 1762 | ### 11.3 Force-Directed Edge Bundling (2 days) |
| 1789 | ### 11.4 Color-Blind Safe Palette (1 day) |
| 1815 | ### 11.5 Orthogonal Layout (1 day) |
| 1839 | ### Tests (Phase 11) |
| 1853 | ## Phase 12: Competitive Parity Plus — Beyond Every Competitor |
| 1857 | ### 12.1 Self-Contained Interactive HTML Export (3 days) |
| 1898 | ### 12.2 Automated Graph Report Generation (2 days) |
| 1929 | ### 12.3 Hub Exclusion Filter (1 day) |
| 1952 | ### 12.4 Surprising/Unexpected Connection Detection (2 days) |
| 1959 | # packages/eoip/graph/surprise.py |
| 1990 | ### 12.5 Rule-Based Conditional Visual Styling (2 days) |
| 2025 | ### 12.6 Lasso/Rectangle Multi-Selection (1 day) |
| 2062 | ### 12.7 URL Deep Linking / Graph State Sharing (2 days) |
| 2098 | ### 12.8 Alternative Table/List View for Accessibility (2 days) |
| 2123 | ### 12.9 Investigation Playbooks (2 days) |
| 2180 | ### 12.10 Cross-Project Graph Merge (2 days) |
| 2187 | # Extend snapshot.py |
| 2208 | ### Tests (Phase 12) |
| 2230 | ## Phase 13: AI-Assisted Graph Intelligence — RAG, Agents & Engineering Disciplines |
| 2234 | ### 13.1 RAG Architecture — 17 Retrieval-Augmented Generation Patterns (1.5 weeks) |
| 2249 | # packages/eoip/rag/base.py |
| 2287 | #### RAG Pattern Implementations |
| 2311 | # apps/api/rag_routes.py |
| 2318 | ### 13.2 Agent Architecture — 40+ Agent Types (1.5 weeks) |
| 2336 | # packages/eoip/agents/base.py |
| 2390 | #### Agent Type Implementations |
| 2407 | # Graph-Aware Tool-Calling Agent |
| 2423 | # Graph Orchestrator Agent |
| 2434 | # Self-Reflection Agent |
| 2450 | # apps/api/agent_routes.py |
| 2458 | ### 13.3 Engineering Disciplines — 8 Graph Intelligence Patterns (1 week) |
| 2472 | # packages/eoip/engineering/loop.py |
| 2499 | # packages/eoip/engineering/graph_eng.py |
| 2520 | # packages/eoip/engineering/harness.py |
| 2542 | # packages/eoip/engineering/memory_eng.py |
| 2571 | # packages/eoip/engineering/context.py |
| 2593 | # packages/eoip/engineering/prompt.py |
| 2618 | # packages/eoip/engineering/composite.py |
| 2653 | # apps/api/engineering_routes.py |
| 2662 | ### 13.4 MCP Integration for Graph Intelligence (3 days) |
| 2668 | # New MCP tools to add to apps/mcp/main.py |
| 2690 | ### 13.5 Frontend: AI Explorer Panel (3 days) |
| 2724 | ### Tests (Phase 13) |
| 2745 | ## Updated Phase Summary |
| 2766 | ## Competitive Advantage Summary |
| 2818 | ## Research Sources Informing This Plan |

### EOIP-engg-doc-pkg/KGR-requirements.md

| Property | Value |
| --- | --- |
| Lines read | 1145 |
| Nonblank lines | 962 |
| SHA-256 prefix | 923ea7e8acea158f |
| First line | # KGR — Knowledge Graph Renderer & Explorer: Requirements Specification |
| Last line | \| Loop-over-Graph \| Pattern where iterative loops progressively refine graph understanding \| |
| Requirement-like lines | 293 |
| Status/gap/risk-like lines | 34 |
| Requirement IDs seen | AC-01, AC-02, AC-03, AC-04, AC-05, AC-06, AC-07, AC-08, AC-09, AC-10, AC-11, AC-12, AC-13, AC-14, AC-15, AC-16, AC-17, AC-18, AC-19, AC-20, AC-21, AC-22, AC-23, AC-24, AC-25, AC-26, AC-27, AC-28, AC-29, AC-30, AC-31, AC-32, AC-33, AC-34, AC-35, AC-36, AC-37, AC-38, AC-39, AC-40 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # KGR — Knowledge Graph Renderer & Explorer: Requirements Specification |
| 10 | ## 1. Executive Summary |
| 14 | ### 1.1 Competitive Positioning — Full Landscape |
| 38 | ### 1.2 Competitor Weaknesses → KGR Strengths |
| 97 | ## 2. Functional Requirements |
| 99 | ### FR-KGR-001: Multi-Graph Type Rendering |
| 103 | #### 2.1 Knowledge Graph (Primary) |
| 112 | #### 2.2 Relationship Graph |
| 120 | #### 2.3 Metadata Graph |
| 129 | #### 2.4 Enterprise Ontology Establishment Graph |
| 138 | #### 2.5 Temporal Graph |
| 146 | #### 2.6 Provenance/Lineage Graph |
| 153 | #### 2.7 Impact/Dependency Graph |
| 162 | #### 2.8 Similarity/Cluster Graph |
| 171 | ### FR-KGR-002: Node Intelligence (8-Tab Inspector) |
| 175 | #### Tab 1: Overview |
| 181 | #### Tab 2: Relationships |
| 189 | #### Tab 3: Impact |
| 199 | #### Tab 4: Evidence |
| 207 | #### Tab 5: Similarity |
| 215 | #### Tab 6: History |
| 221 | #### Tab 7: Annotations |
| 227 | #### Tab 8: Raw |
| 232 | ### FR-KGR-003: Edge Intelligence |
| 244 | ### FR-KGR-004: Interactive Graph Exploration |
| 246 | #### 2.4.1 Navigation |
| 256 | #### 2.4.2 Filtering (10-Dimensional) |
| 275 | #### 2.4.3 Layout Algorithms (12) |
| 295 | #### 2.4.4 Visual Intelligence |
| 306 | ### FR-KGR-005: Data Feed Integration |
| 308 | #### 2.5.1 Live Graph Feed |
| 317 | #### 2.5.2 Search Feed |
| 324 | #### 2.5.3 Query Feed |
| 331 | #### 2.5.4 Analytics Feed |
| 338 | #### 2.5.5 Event Feed Panel |
| 344 | ### FR-KGR-006: Graph Comparison & Diff |
| 354 | ### FR-KGR-007: Export & Sharing (11+ Formats) |
| 373 | ### FR-KGR-008: Annotation & Collaboration |
| 384 | ### FR-KGR-009: AI-Assisted Exploration (Future-Ready) |
| 393 | ### FR-KGR-010: Node Group Collapsing & Combo Declutter |
| 409 | ### FR-KGR-011: Geographic Mode (Geo-Mode) |
| 423 | ### FR-KGR-012: Code + Graph Side-by-Side View |
| 438 | ### FR-KGR-013: Visual Query Builder (No-Code) |
| 453 | ### FR-KGR-014: Dead Code & Orphaned Entity Detection |
| 467 | ### FR-KGR-015: Community Auto-Labeling |
| 479 | ### FR-KGR-016: PR / Change Impact Dashboard |
| 492 | ### FR-KGR-017: Self-Contained Interactive HTML Export |
| 504 | ### FR-KGR-018: Automated Graph Intelligence Report |
| 519 | ### FR-KGR-019: Hub Exclusion Filter |
| 530 | ### FR-KGR-020: Surprising/Unexpected Connection Detection |
| 542 | ### FR-KGR-021: Rule-Based Conditional Visual Styling |
| 553 | ### FR-KGR-022: Lasso/Rectangle Multi-Selection |
| 564 | ### FR-KGR-023: URL Deep Linking / Graph State Sharing |
| 575 | ### FR-KGR-024: Alternative Table/List View (Accessibility) |
| 589 | ### FR-KGR-025: Investigation Playbooks |
| 600 | ### FR-KGR-026: Cross-Project Graph Merge |
| 611 | ### FR-KGR-027: RAG-Powered Graph Intelligence (17 Patterns) |
| 615 | #### 27.1 RAG Patterns |
| 642 | ### FR-KGR-028: Agentic AI Graph Intelligence (40+ Agent Types) |
| 646 | #### 28.1 Agent Categories |
| 666 | ### FR-KGR-029: Engineering Disciplines (8 Patterns) |
| 685 | ### FR-KGR-030: AI Explorer Panel |
| 702 | ## 3. Non-Functional Requirements |
| 704 | ### NFR-KGR-001: Performance |
| 713 | ### NFR-KGR-002: Responsiveness |
| 718 | ### NFR-KGR-003: Accessibility |
| 726 | ### NFR-KGR-004: Browser Support |
| 732 | ### NFR-KGR-005: Security |
| 741 | ## 4. Graph Data Model |
| 743 | ### 4.1 Node Data Contract |
| 770 | ### 4.2 Edge Data Contract |
| 792 | ### 4.3 Blast Radius Result Contract |
| 804 | ### 4.4 Centrality Metrics Contract |
| 819 | ## 5. API Requirements |
| 821 | ### 5.1 Endpoints (Implemented) |
| 831 | ### 5.2 Endpoints (Implemented — Phases 3-10) |
| 853 | ### 5.3 Endpoints (Planned — Phases 12-13) |
| 875 | ### 5.3 Request/Response Contracts |
| 878 | # Blast Radius |
| 883 | # Response: BlastRadiusResult (see 4.3) |
| 885 | # Centrality Metrics |
| 889 | # Response: dict[canonical_id, CentralityMetrics] |
| 891 | # Community Detection |
| 897 | # Response: {communities: [{id, members: [canonical_id], size}], modularity: float} |
| 899 | # What-If Simulation |
| 904 | # Response: {broken_paths: int, orphaned_entities: int, affected_centrality: dict} |
| 906 | # Similarity |
| 912 | # Response: [{canonical_id, score, common_neighbors}] |
| 917 | ## 6. UI/UX Layout |
| 945 | ## 7. Analysis & Intelligence Requirements |
| 947 | ### 7.1 Blast Radius (Implemented) |
| 953 | ### 7.2 Reverse Impact (Implemented) |
| 957 | ### 7.3 Centrality Analysis (Implemented — Phase 3) |
| 969 | ### 7.4 Community Detection (Implemented — Phase 4) |
| 976 | ### 7.5 Similarity Analysis (Implemented — Phase 5) |
| 982 | ### 7.6 Graph Statistics (Implemented — Phases 1+6) |
| 990 | ### 7.7 What-If Analysis (Implemented — Phase 8) |
| 997 | ### 7.8 Anomaly Detection (Implemented — Phase 8) |
| 1004 | ### 7.9 Surprising Connection Analysis (Planned — Phase 12) |
| 1009 | ### 7.10 RAG Intelligence (Planned — Phase 13) |
| 1015 | ### 7.11 Agentic Intelligence (Planned — Phase 13) |
| 1021 | ### 7.12 Engineering Disciplines (Planned — Phase 13) |
| 1028 | ## 8. Acceptance Criteria |
| 1083 | ## 9. Risks & Mitigations |
| 1097 | ## 10. Glossary |

### EOIP-engg-doc-pkg/knowgridflow-product-architecture.md

| Property | Value |
| --- | --- |
| Lines read | 2010 |
| Nonblank lines | 1585 |
| SHA-256 prefix | 40549755cc02fb22 |
| First line | # KnowGridFlow Product Architecture |
| Last line | That contract should remain stable even as connectors, graph domains, models, user experiences and deployment scale evolve. |
| Requirement-like lines | 334 |
| Status/gap/risk-like lines | 14 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # KnowGridFlow Product Architecture |
| 15 | ## 1. Purpose |
| 23 | ### 1.1 Product thesis |
| 27 | ### 1.2 Naming transition |
| 41 | ## 2. Non-Negotiable Architectural Invariants |
| 63 | ## 3. Product Family and Bounded Contexts |
| 88 | ### 3.1 Product boundary rule |
| 104 | ## 4. End-to-End Architecture |
| 169 | ## 5. Kryntara -- Enterprise Knowledge Acquisition Fabric |
| 173 | ### 5.1 Responsibilities |
| 195 | ### 5.2 Non-responsibilities |
| 206 | ### 5.3 Canonical connector interface |
| 221 | ### 5.4 Recommended internal service/module names |
| 238 | ### 5.5 Source waves |
| 268 | ## 6. Canonical `SourceEvent` Contract |
| 272 | ### 6.1 Required semantic fields |
| 297 | ### 6.2 Contract rules |
| 310 | ## 7. Synchryl -- Baseline, Delta and Reconciliation Control |
| 314 | ### 7.1 State model |
| 339 | ### 7.2 Baseline manifest |
| 357 | ### 7.3 Delta processing |
| 377 | ### 7.4 Reconciliation |
| 394 | ## 8. Ontavex -- Semantic Control Plane |
| 398 | ### 8.1 Responsibilities |
| 413 | ### 8.2 Core rule |
| 417 | ### 8.3 Version coupling |
| 435 | ## 9. Idenoryx -- Canonical Identity Resolution |
| 439 | ### 9.1 Resolution order |
| 452 | ### 9.2 Identity artifacts |
| 468 | ### 9.3 Example |
| 485 | ## 10. Vericrya -- Evidence and Provenance |
| 489 | ### 10.1 Evidence model |
| 507 | ### 10.2 Required questions |
| 523 | ## 11. Mutavex -- Graph Evolution Engine |
| 527 | ### 11.1 Revision model |
| 547 | ### 11.2 Relationship replacement |
| 562 | ### 11.3 Deletion semantics |
| 566 | ### 11.4 Graph diff |
| 582 | ## 12. Graphvanta -- Enterprise Knowledge Graph |
| 586 | ### 12.1 Domain graph projections |
| 612 | ### 12.2 Authoritative vs supporting stores |
| 629 | ## 13. Semantic Change Journal and Event Bus |
| 631 | ### 13.1 Semantic Change Journal |
| 655 | ### 13.2 Semantic Event Bus |
| 672 | ## 14. Temporiq -- Enterprise Time Machine |
| 676 | ### 14.1 Required capabilities |
| 690 | ### 14.2 Example questions |
| 700 | ## 15. Archovex -- Architecture Intelligence |
| 704 | ### 15.1 Three-state model |
| 714 | ### 15.2 Findings |
| 727 | ### 15.3 Architecture-as-graph |
| 733 | ## 16. Knovigil -- Knowledge Health and Knowledge Debt |
| 737 | ### 16.1 Finding categories |
| 760 | ### 16.2 Knowledge SLOs |
| 776 | ## 17. Polivex -- Governance Control Plane |
| 780 | ### 17.1 Policy domains |
| 796 | ### 17.2 Decision contract |
| 815 | ## 18. Quorvyn -- Search, Retrieval and Reasoning |
| 819 | ### 18.1 Retrieval modes |
| 832 | ### 18.2 Query semantics |
| 848 | ### 18.3 Answer contract |
| 867 | ## 19. Causoryn -- Causal and Impact Intelligence |
| 871 | ### 19.1 Capabilities |
| 883 | ### 19.2 Example path |
| 904 | ## 20. Simuvexa -- Counterfactual Enterprise Twin |
| 908 | ### 20.1 Isolation rule |
| 923 | ### 20.2 Example scenarios |
| 934 | ### 20.3 Scenario output |
| 949 | ## 21. Agenthyr -- Governed Agentic Intelligence |
| 953 | ### 21.1 Candidate agents |
| 973 | ### 21.2 Agent rules |
| 986 | ## 22. Capsoryn -- Knowledge Capsules |
| 990 | ### 22.1 Capsule content |
| 1012 | ### 22.2 Consumers |
| 1027 | ## 23. Lensoryx -- Unified Experience Platform |
| 1031 | ### 23.1 Required lenses |
| 1054 | ### 23.2 Shared lens context |
| 1070 | ### 23.3 Graph canvas capabilities |
| 1088 | ### 23.4 Graph playback |
| 1101 | ## 24. Public API Architecture |
| 1105 | ### 24.1 API groups |
| 1127 | ### 24.2 API principles |
| 1140 | ## 25. Internal Event Taxonomy |
| 1179 | ## 26. Data and Storage Topology |
| 1181 | ### 26.1 Minimal self-hosted MVP |
| 1207 | ### 26.2 Scale-out only when justified |
| 1223 | ## 27. Deployment Architecture |
| 1225 | ### 27.1 Docker Compose target |
| 1242 | ### 27.2 Air-gapped posture |
| 1257 | ## 28. Security Architecture |
| 1259 | ### 28.1 Trust boundaries |
| 1271 | ### 28.2 Security controls |
| 1290 | ## 29. Observability Architecture |
| 1305 | ### 29.1 Per-source metrics |
| 1320 | ### 29.2 Graph evolution metrics |
| 1333 | ## 30. Repository Structure |
| 1420 | ### 30.1 Dependency direction |
| 1439 | ## 31. Core Processing Sequence |
| 1441 | ### 31.1 New source onboarding |
| 1459 | ### 31.2 Incremental update |
| 1479 | ### 31.3 Failure rule |
| 1485 | ## 32. Requirement-to-Product Mapping |
| 1513 | ## 33. Phase-to-Product Mapping |
| 1515 | ### G2-P0 -- Contract & Architecture Alignment |
| 1538 | ### G2-P1 -- Acquisition Fabric Core |
| 1558 | ### G2-P2 -- Baseline + Incremental Graph Evolution |
| 1579 | ### G2-P3 -- Source Wave 1 |
| 1587 | ### G2-P4 -- Source Wave 2 |
| 1596 | ### G2-P5 -- Source Wave 3 |
| 1607 | ### G2-P6 -- Expanded Semantic Digital Twin |
| 1622 | ### G2-P7 -- Temporal, Architecture and Process Intelligence |
| 1631 | ### G2-P8 -- Knowledge Health and Governed AI |
| 1641 | ### G2-P9 -- Simulation and Causal Intelligence |
| 1650 | ### G2-P10 -- Diamond-Standard UX and Production Hardening |
| 1669 | ## 34. MVP / Pilot Boundary |
| 1673 | ### 34.1 Recommended pilot minimum |
| 1685 | ### 34.2 Pilot demo narrative |
| 1706 | ## 35. Acceptance Gates by Architecture Layer |
| 1708 | ### Gate A -- Contract integrity |
| 1715 | ### Gate B -- Synchronization integrity |
| 1724 | ### Gate C -- Historical integrity |
| 1732 | ### Gate D -- Provenance integrity |
| 1739 | ### Gate E -- Cross-source intelligence |
| 1745 | ### Gate F -- Production operability |
| 1756 | ## 36. Testing Strategy |
| 1758 | ### 36.1 Contract tests |
| 1765 | ### 36.2 Connector tests |
| 1780 | ### 36.3 Evolution tests |
| 1791 | ### 36.4 Identity tests |
| 1799 | ### 36.5 Security tests |
| 1810 | ### 36.6 End-to-end golden scenarios |
| 1821 | ## 37. Architecture Decision Records Required Early |
| 1843 | ## 38. Anti-Patterns to Reject |
| 1866 | ## 39. Product Positioning Boundary |
| 1895 | ## 40. Engineering Priorities |
| 1912 | ## 41. Immediate Next Implementation Backlog |
| 1916 | ### Priority 0 |
| 1925 | ### Priority 1 |
| 1933 | ### Priority 2 |
| 1942 | ### Priority 3 |
| 1952 | ## 42. Definition of Architecture Complete |
| 1973 | ## 43. Final Architecture Statement |

### EOIP-engg-doc-pkg/MVP-implementation-plan.md

| Property | Value |
| --- | --- |
| Lines read | 590 |
| Nonblank lines | 533 |
| SHA-256 prefix | f47280f32166d976 |
| First line | # MVP Implementation Plan |
| Last line | A task is DONE only when implementation exists, interfaces are documented, automated tests pass, failure paths/logging/configuration/security are addressed, acceptance criteria pass and the requirement→component→task→test→acceptance traceability entry exists. The MVP is DONE only after T28 executes from a clean documented environment and the backup/restore cycle reproduces golden queries. |
| Requirement-like lines | 204 |
| Status/gap/risk-like lines | 4 |
| Requirement IDs seen | FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020, FR-021, FR-022, FR-023, FR-024, FR-025, FR-026, FR-027, FR-028, FR-ADMIN-001, FR-ADMIN-002, FR-AGENT-003, FR-CODE-001, FR-CODE-002, FR-CODE-004, FR-CONN-002, FR-CONN-003, FR-CONN-004, FR-GRAPH-001, FR-GRAPH-002, FR-GRAPH-003 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # MVP Implementation Plan |
| 11 | ## Architecture baseline |
| 14 | ## Architecture decisions |
| 28 | ## Repository structure |
| 77 | ## Service boundaries |
| 91 | ## Build dependency graph |
| 123 | ## Implementation tasks |
| 125 | ### T01 — HugeGraph foundation |
| 141 | ### T02 — Schema bootstrap |
| 157 | ### T03 — Jira JSON connector |
| 173 | ### T04 — Git/GitLab ingestion |
| 189 | ### T05 — Code parsing |
| 205 | ### T06 — Canonical model |
| 221 | ### T07 — Jira graph |
| 236 | ### T08 — Code graph |
| 251 | ### T09 — Meta graph |
| 266 | ### T10 — Cross-domain semantic linker |
| 282 | ### T11 — Provenance |
| 298 | ### T12 — Validation and quality |
| 313 | ### T13 — Query API |
| 329 | ### T14 — Impact analysis |
| 345 | ### T15 — Path query |
| 360 | ### T16 — Search/query web experience |
| 375 | ### T17 — Graph visualizer |
| 390 | ### T18 — Admin ingestion/validation UI |
| 405 | ### T19 — VS Code extension |
| 421 | ### T20 — Local GraphRAG |
| 437 | ### T21 — TraceImpactAgent |
| 453 | ### T22 — MCP read server |
| 468 | ### T23 — Structured logging |
| 483 | ### T24 — Metrics and health |
| 498 | ### T25 — Backup |
| 514 | ### T26 — Restore |
| 530 | ### T27 — Automated test system |
| 546 | ### T28 — End-to-end demo release |
| 563 | ## Security controls |
| 566 | ## Phase 1 security baseline |
| 579 | ## Performance gate |
| 582 | ## MVP benchmark definition (targets, not measured claims) |
| 588 | ## Definition of done |

### EOIP-engg-doc-pkg/MVP-requirements.md

| Property | Value |
| --- | --- |
| Lines read | 275 |
| Nonblank lines | 221 |
| SHA-256 prefix | 18ab7fb37df6b910 |
| First line | # MVP Requirements |
| Last line | Phase 1 exits only when a fresh clone/offline-ready package can execute `docker compose up`, become ready, initialize schema, ingest the fixtures, pass automated tests, run the documented demo, create a backup, destroy/recreate graph state, restore it, and rerun golden trace/impact queries successfully. |
| Requirement-like lines | 147 |
| Status/gap/risk-like lines | 1 |
| Requirement IDs seen | FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020, FR-021, FR-022, FR-023, FR-024, FR-025, FR-026, FR-027, FR-028, FR-ADMIN-001, FR-ADMIN-002, FR-AGENT-003, FR-CODE-001, FR-CODE-002, FR-CODE-004, FR-CONN-002, FR-CONN-003, FR-CONN-004, FR-GRAPH-001, FR-GRAPH-002, FR-GRAPH-003 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # MVP Requirements |
| 11 | ## Product outcome |
| 19 | ## Non-negotiable MVP boundaries |
| 29 | ## Runtime architecture |
| 66 | ## Mandatory MVP capabilities |
| 68 | ### MVP-FR-001 — Apache HugeGraph local Docker |
| 74 | ### MVP-FR-002 — Automatic graph schema initialization |
| 80 | ### MVP-FR-003 — Jira JSON ingestion |
| 86 | ### MVP-FR-004 — Git repository/GitLab ingestion |
| 92 | ### MVP-FR-005 — Code parsing |
| 98 | ### MVP-FR-006 — Canonical entity generation |
| 104 | ### MVP-FR-007 — Jira graph |
| 110 | ### MVP-FR-008 — Code graph |
| 116 | ### MVP-FR-009 — Meta graph |
| 122 | ### MVP-FR-010 — Cross-graph linking |
| 128 | ### MVP-FR-011 — Provenance |
| 134 | ### MVP-FR-012 — Graph validation |
| 140 | ### MVP-FR-013 — Query API |
| 146 | ### MVP-FR-014 — Impact analysis query |
| 152 | ### MVP-FR-015 — Path query |
| 158 | ### MVP-FR-016 — Search/query UI |
| 164 | ### MVP-FR-017 — Graph visualizer |
| 170 | ### MVP-FR-018 — Admin ingestion/validation UI |
| 176 | ### MVP-FR-019 — VS Code extension |
| 182 | ### MVP-FR-020 — Local GraphRAG |
| 188 | ### MVP-FR-021 — Useful read-only agent workflow |
| 194 | ### MVP-FR-022 — MCP core graph access |
| 200 | ### MVP-FR-023 — Logging |
| 206 | ### MVP-FR-024 — Metrics |
| 212 | ### MVP-FR-025 — Backup |
| 218 | ### MVP-FR-026 — Restore |
| 224 | ### MVP-FR-027 — Automated tests |
| 230 | ### MVP-FR-028 — End-to-end demo |
| 236 | ## Demo flow |
| 253 | ## Phase 1 security baseline |
| 267 | ## MVP benchmark definition (targets, not measured claims) |
| 273 | ## MVP exit gate |

### EOIP-engg-doc-pkg/README.md

| Property | Value |
| --- | --- |
| Lines read | 49 |
| Nonblank lines | 37 |
| SHA-256 prefix | fa49b45b12511926 |
| First line | # Enterprise Ontology & Intelligence Platform (EOIP) — Engineering Documentation Package |
| Last line | - Performance targets remain targets until benchmarked on declared hardware/data. |
| Requirement-like lines | 13 |
| Status/gap/risk-like lines | 1 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Enterprise Ontology & Intelligence Platform (EOIP) — Engineering Documentation Package |
| 8 | ## Start here |
| 21 | ## MVP architecture in one sentence |
| 25 | ## Important scope truth |
| 29 | ## Directories |
| 38 | ## Architecture invariants |

### examples/demo-enterprise/README.md

| Property | Value |
| --- | --- |
| Lines read | 28 |
| Nonblank lines | 19 |
| SHA-256 prefix | d0d1e3a5fe417883 |
| First line | # Northstar enterprise demo pack |
| Last line | Every scenario reports `ready: true` only when each expected graph entity is actually present. |
| Requirement-like lines | 7 |
| Status/gap/risk-like lines | 1 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Northstar enterprise demo pack |
| 5 | ## What is included |
| 15 | ## Quick verification |

### examples/demo-enterprise/wiki/checkout-latency-runbook.md

| Property | Value |
| --- | --- |
| Lines read | 12 |
| Nonblank lines | 9 |
| SHA-256 prefix | bd18c1105504516c |
| First line | # Checkout latency incident runbook |
| Last line | Rollback authority belongs to Commerce SRE. Emergency changes require an auditable ServiceNow approval. |
| Requirement-like lines | 3 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Checkout latency incident runbook |

### examples/demo-enterprise/wiki/checkout-risk-architecture.md

| Property | Value |
| --- | --- |
| Lines read | 34 |
| Nonblank lines | 23 |
| SHA-256 prefix | d95bc157842bc188 |
| First line | # Checkout risk architecture |
| Last line | TC-884 proves the low-risk contract and TC-901 proves timeout behavior. Pipeline 4815 must complete contract tests before the production deployment job can run. |
| Requirement-like lines | 5 |
| Status/gap/risk-like lines | 5 |
| Requirement IDs seen | ADR-COM-014 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Checkout risk architecture |
| 8 | ## Context |
| 12 | ## Runtime flow |
| 20 | ## Reliability boundary |
| 24 | ## Failure modes and safe fallback |
| 32 | ## Verification |

### examples/demo-repo/README.md

| Property | Value |
| --- | --- |
| Lines read | 4 |
| Nonblank lines | 3 |
| SHA-256 prefix | b23a7c8fb1478172 |
| First line | # EOIP-1 requirement trace |
| Last line | the Python math module. EOIP-2 requires the path to retain source evidence. |
| Requirement-like lines | 1 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen | EOIP-1, EOIP-2 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP-1 requirement trace |

### handoff_template.md

| Property | Value |
| --- | --- |
| Lines read | 39 |
| Nonblank lines | 36 |
| SHA-256 prefix | 414c79298224ac20 |
| First line | # EOIP Handoff Template |
| Last line | file/section references are preferable to stale hardcoded line numbers. |
| Requirement-like lines | 3 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Handoff Template |

### instruction.md

| Property | Value |
| --- | --- |
| Lines read | 140 |
| Nonblank lines | 113 |
| SHA-256 prefix | 60e70b0d3ede0845 |
| First line | # EOIP Agent Orchestration Instructions and Contracts |
| Last line | agents must not independently weaken enforcement rules to make their work pass. |
| Requirement-like lines | 22 |
| Status/gap/risk-like lines | 13 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Agent Orchestration Instructions and Contracts |
| 12 | ## Sources of truth and synchronization |
| 35 | ## Read and scope contract |
| 52 | ## Role and execution contract |
| 65 | ## Ticket and status contract |
| 88 | ## Verification, safety and publication |
| 104 | ## Session lifecycle and handoff |
| 122 | ## Resume prompt |

### memory.md

| Property | Value |
| --- | --- |
| Lines read | 326 |
| Nonblank lines | 275 |
| SHA-256 prefix | c3e3e53d2216bb17 |
| First line | # EOIP Coordination Memory |
| Last line | --- HANDOFF END --- |
| Requirement-like lines | 94 |
| Status/gap/risk-like lines | 39 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Coordination Memory |
| 16 | ## Session start and reconciliation |
| 49 | ## Evidence observed, not rerun |
| 73 | ## Retained historical template/proposal notes |
| 87 | ## Prior handoff - coordination packet |
| 123 | ## Prior handoff - validation evidence foundation |
| 154 | ## Prior handoff - full documentation gap scan |
| 183 | ## Prior handoff - MVP gap implementation closure before extension rerun |
| 212 | ## Prior handoff - MVP acceptance continuation |
| 241 | ## Prior handoff - full console repair |
| 270 | ## Prior handoff - VS Code source-extension demo |
| 299 | ## Latest handoff |

### onboarding_checklist.md

| Property | Value |
| --- | --- |
| Lines read | 27 |
| Nonblank lines | 24 |
| SHA-256 prefix | e471f62f5d43279c |
| First line | # EOIP Onboarding Checklist |
| Last line | automatic re-onboarding or compulsory creation of three tickets. |
| Requirement-like lines | 3 |
| Status/gap/risk-like lines | 1 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Onboarding Checklist |

### onboarding_prompts.md

| Property | Value |
| --- | --- |
| Lines read | 71 |
| Nonblank lines | 56 |
| SHA-256 prefix | 5683270bbb484534 |
| First line | # EOIP Onboarding and Resume Prompts |
| Last line | come from [instruction](instruction.md), not from a shortened prompt. |
| Requirement-like lines | 7 |
| Status/gap/risk-like lines | 5 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Onboarding and Resume Prompts |
| 7 | ## One-time prompt: ONBOARD-AND-RECONCILE |
| 43 | ## Short resume prompt |
| 59 | ## Explicit bounded assignment |

### README.md

| Property | Value |
| --- | --- |
| Lines read | 117 |
| Nonblank lines | 98 |
| SHA-256 prefix | de063f7145110438 |
| First line | # EOIP — Enterprise Ontology & Intelligence Platform |
| Last line | bounded orchestration, evidence-linked explanations, and approval-only change proposals. |
| Requirement-like lines | 50 |
| Status/gap/risk-like lines | 5 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP — Enterprise Ontology & Intelligence Platform |
| 18 | ## Quick Start |
| 49 | ## Documentation |
| 70 | ## On-prem source connectors |
| 101 | ## RDF/OWL interoperability |

### roles.md

| Property | Value |
| --- | --- |
| Lines read | 526 |
| Nonblank lines | 437 |
| SHA-256 prefix | c28e5068f007c156 |
| First line | # EOIP Application Roles, Activities and Persona Lines |
| Last line | Product Manager accepts scope and the designated human authority approves release. |
| Requirement-like lines | 199 |
| Status/gap/risk-like lines | 24 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Application Roles, Activities and Persona Lines |
| 19 | ## 1. Constraints every role must preserve |
| 48 | ## 2. Shared working agreement |
| 50 | ### Assignment and ownership |
| 70 | ### Activities throughout delivery |
| 81 | ### Evidence and definition of done |
| 99 | ## 3. Strategy, product and delivery roles |
| 101 | ### Chief Executive Officer (CEO) |
| 107 | ### Chief Technology Officer (CTO) |
| 113 | ### Chief Operating Officer (COO) |
| 119 | ### Chief Financial Officer (CFO) |
| 125 | ### Chief Marketing Officer (CMO) |
| 131 | ### Product Manager |
| 137 | ### Business Analyst |
| 143 | ### Analyst |
| 149 | ### Project Manager |
| 155 | ### Scrum Master |
| 161 | ### Stakeholder |
| 167 | ### Consultant |
| 173 | ## 4. Architecture and engineering leadership |
| 175 | ### Architect |
| 181 | ### Enterprise and Solution Architect (**New**) |
| 187 | ### Lead Developer |
| 193 | ### Senior Engineer |
| 199 | ### Developer |
| 205 | ### Intern |
| 211 | ## 5. Graph, source and data specialists |
| 213 | ### Knowledge Graph and Ontology Engineer (**New**) |
| 219 | ### Data Engineer |
| 225 | ### Connector and Integration Engineer (**New**) |
| 231 | ### Code Intelligence and Parser Engineer (**New**) |
| 237 | ### Database Administrator |
| 243 | ### Data Steward (**New**) |
| 249 | ### Query and Graph Analytics Engineer (**New**) |
| 255 | ## 6. User experiences and protocol engineering |
| 257 | ### UX Designer |
| 263 | ### Frontend and Admin UI Engineer (**New**) |
| 269 | ### Graph Visualization Engineer (**New**) |
| 275 | ### VS Code Extension Engineer (**New**) |
| 281 | ### Backend and API Engineer (**New**) |
| 287 | ### MCP and Tooling Engineer (**New**) |
| 293 | ## 7. Local AI, agents and evaluation |
| 295 | ### LLM Orchestrator |
| 301 | ### Local AI and Model Engineer (**New**) |
| 307 | ### GraphRAG and Retrieval Engineer (**New**) |
| 313 | ### Agent Runtime and Workflow Engineer (**New**) |
| 319 | ### Memory and Context Engineer (**New**) |
| 325 | ### Human-Control and Automation Engineer (**New**) |
| 331 | ### AI Evaluation and Explainability Engineer (**New**) |
| 337 | ## 8. Quality, security and governance |
| 339 | ### QA Lead |
| 345 | ### Tester |
| 351 | ### Security Officer |
| 357 | ### Compliance Officer |
| 363 | ### Data Privacy Officer |
| 369 | ### Ethics Officer |
| 375 | ### Legal Advisor |
| 381 | ## 9. Operations, recovery and release |
| 383 | ### DevOps Engineer |
| 389 | ### System Administrator |
| 395 | ### Network Engineer |
| 401 | ### Site Reliability Engineer (SRE) (**New**) |
| 407 | ### Performance and Scalability Engineer (**New**) |
| 413 | ### Recovery and Data Integrity Engineer (**New**) |
| 419 | ### Release and Software Supply Chain Engineer (**New**) |
| 425 | ### Technical Writer (**New**) |
| 431 | ### Customer Enablement and Support Engineer (**New**) |
| 437 | ### Demo Producer |
| 443 | ## 10. Cross-functional accountability and handoffs |
| 473 | ## 11. Phase activation and smallest practical team |
| 497 | ## 12. Role assignment and handoff template |

### secrets.example/README.md

| Property | Value |
| --- | --- |
| Lines read | 24 |
| Nonblank lines | 17 |
| SHA-256 prefix | a8feb4a87029e4fb |
| First line | # Secrets Directory |
| Last line | **Never commit actual secrets to version control.** |
| Requirement-like lines | 4 |
| Status/gap/risk-like lines | 0 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # Secrets Directory |
| 5 | ## Files |
| 10 | ## Usage |

### tickets/requirements-map.md

| Property | Value |
| --- | --- |
| Lines read | 28 |
| Nonblank lines | 24 |
| SHA-256 prefix | b1298e7d2c2830f6 |
| First line | # EOIP Requirements and Coordination Map |
| Last line | limited by scope exclusions, live evidence and independent release gates. |
| Requirement-like lines | 8 |
| Status/gap/risk-like lines | 5 |
| Requirement IDs seen | FR-001, FR-027, FR-028, REQ-USER-IMPORT-001 |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Requirements and Coordination Map |
| 17 | ## Mapping rules |

### tickets/ticket-20261004-001.md

| Property | Value |
| --- | --- |
| Lines read | 83 |
| Nonblank lines | 59 |
| SHA-256 prefix | 2f7fca404abf1f6e |
| First line | **ID**: ticket-20261004-001 |
| Last line | - 2026-10-04T11:27:25.1113901+05:30 — Reconciled supplied proposal: In Progress/P0 -> Blocked/P2; no valid requirement/spec/stub found; Product Manager owns scope review. Prior person/branch claims preserved as unverified. Queue/checklist/map/context/memory synchronized. |
| Requirement-like lines | 14 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 30 | ## Reconciliation - 2026-10-04 |
| 51 | ## Original proposal (retained, not approved or executable) |

### tickets/ticket-20261004-002.md

| Property | Value |
| --- | --- |
| Lines read | 61 |
| Nonblank lines | 54 |
| SHA-256 prefix | c678640944c63915 |
| First line | **ID**: ticket-20261004-002 |
| Last line | - 2026-10-04 — In Progress -> Done after passing packet consistency checks; queue/checklist/map/context/memory aligned. Working-tree edits only; no application completion claim. |
| Requirement-like lines | 5 |
| Status/gap/risk-like lines | 4 |
| Requirement IDs seen |  |

Headings: none.

### tickets/ticket-20261004-003.md

| Property | Value |
| --- | --- |
| Lines read | 110 |
| Nonblank lines | 102 |
| SHA-256 prefix | 21ad600d2671b653 |
| First line | **ID**: ticket-20261004-003 |
| Last line | validation passed with 5 slides, 12 XML parts and `zip_bad=None`. |
| Requirement-like lines | 33 |
| Status/gap/risk-like lines | 24 |
| Requirement IDs seen | FR-001, FR-028 |

Headings: none.

### tickets/ticket-20261004-004.md

| Property | Value |
| --- | --- |
| Lines read | 66 |
| Nonblank lines | 59 |
| SHA-256 prefix | 67ae81d49e282cdb |
| First line | **ID**: ticket-20261004-004 |
| Last line | remains Blocked for remote CI, publication and independent phase review only. |
| Requirement-like lines | 13 |
| Status/gap/risk-like lines | 5 |
| Requirement IDs seen | FR-027 |

Headings:
| Line | Heading |
| --- | --- |
| 14 | ## Verified gap and scope |
| 26 | ## Acceptance criteria |

### tickets/ticket-20261004-005.md

| Property | Value |
| --- | --- |
| Lines read | 109 |
| Nonblank lines | 105 |
| SHA-256 prefix | b90cd30f943b1649 |
| First line | **ID**: ticket-20261004-005 |
| Last line | and live-stack verification remain pending. |
| Requirement-like lines | 35 |
| Status/gap/risk-like lines | 2 |
| Requirement IDs seen |  |

Headings: none.

### tickets/ticket-template.md

| Property | Value |
| --- | --- |
| Lines read | 38 |
| Nonblank lines | 35 |
| SHA-256 prefix | 01a97139f1c81bf2 |
| First line | # EOIP Ticket Template |
| Last line | approval stays pending until actually supplied. |
| Requirement-like lines | 4 |
| Status/gap/risk-like lines | 6 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Ticket Template |

### todo-status.md

| Property | Value |
| --- | --- |
| Lines read | 33 |
| Nonblank lines | 27 |
| SHA-256 prefix | 949d82469a6a472d |
| First line | # EOIP Ticket Queue |
| Last line | in [memory](memory.md), not executable backlog, assigned commitments or agreed ETAs. |
| Requirement-like lines | 6 |
| Status/gap/risk-like lines | 8 |
| Requirement IDs seen |  |

Headings:
| Line | Heading |
| --- | --- |
| 1 | # EOIP Ticket Queue |
| 21 | ## Milestone boundaries |

## Per-ID Core Requirement Registers

Added 2026-10-07 from an independent cross-audit. ID, title, and priority come from the defining documents as read line-by-line (READER A digest of `EOIP-engg-doc-pkg/03-functional-requirements.md` and `04-non-functional-requirements.md`; READER E digest of `EOIP-engg-doc-pkg/MVP-requirements.md`). Current status follows the declared "local code/test-evidence audit policy" of `docs/audit-2026-10-06/assessed-gap-report.md` (sections 1, 2, and 12: all 67 FR, 14 NFR, and 28 MVP-FR rows marked Done). The evidence tier is the honest qualification: `tested` = real modules backed by automated tests (AUDIT-CODE found no stubs or TODO-passed-as-done in the core FR/NFR/MVP rows); `exists` = implementation exists but the linkage or assertion is weaker than behavioral proof; `external gate` = an acceptance step outside the local code base (live tenants, production infrastructure, certification) remains open. Note: the per-ID Done statuses rest on the assessed report's policy, not on independent re-execution of every behavior — see "Honest Code-Evidence Verdict" below for what that policy actually measures.

### FR register (67 IDs; defining doc: `EOIP-engg-doc-pkg/03-functional-requirements.md`)

| ID | Title | Priority | Defining doc | Current status (audit policy) | Evidence tier |
| --- | --- | --- | --- | --- | --- |
| FR-CONN-001 | Connector SDK | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-CONN-002 | Jira JSON connector | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested (fixture); live Jira tenant = external gate |
| FR-CONN-003 | Git repository connector | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-CONN-004 | GitLab metadata adapter | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested (fixture); live GitLab tenant = external gate |
| FR-CONN-005 | Connector resiliency | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-CONN-006 | Dry run and replay | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-CONN-007 | Source deletion semantics | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-CONF-001 | Confluence connector | P2 | 03-functional-requirements.md | Done (code-evidence policy; ahead of its P2 target phase) | tested (fixture); live Confluence tenant = external gate |
| FR-SNOW-001 | ServiceNow connector | P2 | 03-functional-requirements.md | Done (code-evidence policy; ahead of its P2 target phase) | tested (fixture); live ServiceNow tenant = external gate |
| FR-INGEST-001 | Raw capture | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-INGEST-002 | Canonicalization | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-INGEST-003 | Idempotent mutation | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-INGEST-004 | Ingestion job lifecycle | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-INGEST-005 | Dead-letter processing | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-GRAPH-001 | HugeGraph authoritative store | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested; normative wording amended by 06-architecture.md multi-backend decision (see Contradictions) |
| FR-GRAPH-002 | Logical graph domains | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested; as-built domain list (14 named domains in 06) differs from this FR's illustrative list (see Contradictions) |
| FR-GRAPH-003 | Schema bootstrap | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-GRAPH-004 | Canonical identifiers | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-GRAPH-005 | Meta graph | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-GRAPH-006 | Cross-domain bridge edges | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-GRAPH-007 | Gremlin repository | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested; named-template model now abstracts over multiple backends per 76-multi-backend.md |
| FR-GRAPH-008 | Index strategy | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested; note UNIQUE edge index not honored by HugeGraph 1.7, migrated to SECONDARY + edge_key sort key (docs/benchmarking.md) |
| FR-GRAPH-009 | Graph version journal | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested; full snapshots/diffs remain P5 scope |
| FR-GRAPH-010 | RDF/OWL interoperability | P2 | 03-functional-requirements.md | Done (code-evidence policy; ahead of its P2 target phase) | tested (JSON-LD export via ontology/rdf.py, verified by AUDIT-CODE) |
| FR-ONTO-001 | Enterprise ontology vocabulary | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-ONTO-002 | Relationship semantics | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-PROV-001 | Evidence model | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-PROV-002 | Provenance traversal | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-ID-001 | Deterministic identity resolution | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-ID-002 | Ambiguous identity candidates | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-TEMP-001 | Bitemporal-ready fields | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested; current-state queries only in MVP, temporal reconstruction is P5 scope |
| FR-CODE-001 | Deterministic code parser | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-CODE-002 | Python and TypeScript MVP parsing | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-CODE-003 | Commit-to-symbol linking | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy; flipped from Partial in Pass 8 per assessed report section 3) | tested |
| FR-CODE-004 | Call/import/dependency edges | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-CODE-005 | Source navigation | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-QUERY-001 | Structured QueryPlan | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-QUERY-002 | Path query | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-QUERY-003 | Impact analysis | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-QUERY-004 | Entity search | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-QUERY-005 | Natural-language query interpretation | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-QUERY-006 | Query safety policy | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-QUERY-007 | Query evidence envelope | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-QUERY-008 | Raw Gremlin admin boundary | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy; flipped from Partial in Pass 8 per assessed report section 3) | tested (admin gate on EOIP_ADMIN_GREMLIN_ENABLED verified at apps/api/main.py) |
| FR-VALID-001 | Graph validation rules | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-VALID-002 | Validation gates | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-VALID-003 | Graph quality metrics | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-RAG-001 | Retrieval router | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested (17 routing patterns confirmed by AUDIT-CODE) |
| FR-RAG-002 | GraphRAG evidence retrieval | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-RAG-003 | Local model abstraction | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-RAG-004 | No mandatory vector DB in MVP | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-RAG-005 | RAG evaluation harness | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-RAG-006 | Adaptive RAG strategy framework | P3 | 03-functional-requirements.md | Done (code-evidence policy; ahead of its P3 target phase) | exists (strategy plugin interface + 4 built-in strategies verified; full adaptive catalog beyond MVP evidence) |
| FR-AGENT-001 | Agent contract | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-AGENT-002 | Bounded agent runtime | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested (READ_TOOLS enforcement, budgets, circuit breaker verified by AUDIT-CODE) |
| FR-AGENT-003 | TraceImpact agent | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-AGENT-004 | Write/action approval boundary | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-AGENT-005 | Controlled self-modification | P8+ | 03-functional-requirements.md | Done (code-evidence policy; flipped from Partial in Pass 8) | exists (absence/negative assertion; AUDIT-CODE notes the cited evidence mischaracterizes agents/governed.py, which is actually an 11-agent specialist library) |
| FR-MEM-001 | Scoped memory records | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested; completion signal ("no uncontrolled accumulation") is qualitative per the defining docs |
| FR-MCP-001 | MCP read server | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested (18 tools implemented; doc drift on the count, see Contradictions) |
| FR-MCP-002 | MCP action separation | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-UI-001 | User web application | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested (Playwright suite recorded passed 2026-10-06) |
| FR-UI-002 | Graph explorer | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-ADMIN-001 | Admin ingestion UI | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-ADMIN-002 | Admin graph quality UI | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested |
| FR-VSCODE-001 | VS Code context extension | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested (extension-host tests); installed-VSIX acceptance = external gate |
| FR-VSCODE-002 | VS Code trace/impact commands | P1-MVP | 03-functional-requirements.md | Done (code-evidence policy) | tested; installed-VSIX acceptance = external gate |

### NFR register (14 IDs; defining doc: `EOIP-engg-doc-pkg/04-non-functional-requirements.md`)

| ID | Title | Priority | Defining doc | Current status (audit policy) | Evidence tier |
| --- | --- | --- | --- | --- | --- |
| NFR-SEC-001 | No outbound enterprise-data egress | P1-MVP | 04-non-functional-requirements.md | Done (code-evidence policy) | tested (tests/security suite green, 27 tests) |
| NFR-SEC-002 | Secret isolation | P1-MVP | 04-non-functional-requirements.md | Done (code-evidence policy) | tested |
| NFR-SEC-003 | Input/file safety | P1-MVP | 04-non-functional-requirements.md | Done (code-evidence policy) | tested |
| NFR-SEC-004 | Prompt/tool injection defenses | P1-MVP | 04-non-functional-requirements.md | Done (code-evidence policy) | tested |
| NFR-SEC-005 | Authentication without MVP RBAC | P1-MVP | 04-non-functional-requirements.md | Done (code-evidence policy) | tested; independent security certification = external gate |
| NFR-SEC-006 | Container hardening | P1-MVP | 04-non-functional-requirements.md | Done (code-evidence policy) | tested (9 hardening tests; report said 8, under-counted) |
| NFR-SEC-007 | Audit events | P1-MVP | 04-non-functional-requirements.md | Done (code-evidence policy) | tested |
| NFR-REL-001 | Restart-safe processing | P1-MVP | 04-non-functional-requirements.md | Done (code-evidence policy) | tested |
| NFR-REL-002 | Backup and restore | P1-MVP | 04-non-functional-requirements.md | Done (code-evidence policy) | tested (logical/checksummed backup + restore receipts); native HugeGraph backup and crash-atomic multi-store recovery = external gate |
| NFR-OPS-001 | Structured logging and health | P1-MVP | 04-non-functional-requirements.md | Done (code-evidence policy; flipped from Partial in Pass 8) | tested (/health/live + /health/ready live-verified 200; note the report's evidence path is the observability/ package, not a single observability.py file) |
| NFR-OPS-002 | Local metrics | P1-MVP | 04-non-functional-requirements.md | Done (code-evidence policy; flipped from Partial in Pass 8) | tested (/metrics live-verified 200) |
| NFR-PERF-001 | Benchmark-defined objectives | P1-MVP | 04-non-functional-requirements.md | Done (code-evidence policy) — CONTESTED: docs/benchmarking.md (also current) says the full-profile isolated-HugeGraph acceptance "remains partially open" | memory-profile benchmarks tested; production-scale/hardware-backed benchmark = external gate |
| NFR-MAINT-001 | Modular monolith boundary | P1-MVP | 04-non-functional-requirements.md | Done (code-evidence policy) | tested |
| NFR-PRIV-001 | Data minimization and classification | P1-MVP | 04-non-functional-requirements.md | Done (code-evidence policy) | tested |

### MVP register (28 IDs; defining doc: `EOIP-engg-doc-pkg/MVP-requirements.md`, tasks T01-T28 in `MVP-implementation-plan.md`)

| ID | Title | Parent requirements | Priority | Defining doc | Current status (audit policy) | Evidence tier |
| --- | --- | --- | --- | --- | --- | --- |
| MVP-FR-001 | HugeGraph local Docker | FR-GRAPH-001 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested (stack live-verified healthy) |
| MVP-FR-002 | Automatic schema initialization | FR-GRAPH-003 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested |
| MVP-FR-003 | Jira JSON ingestion | FR-CONN-002 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested (fixture) |
| MVP-FR-004 | Git/GitLab ingestion | FR-CONN-003/004 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested (fixture) |
| MVP-FR-005 | Code parsing, no LLM | FR-CODE-001/002 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested |
| MVP-FR-006 | Canonical entity generation, idempotent | FR-INGEST-002, FR-GRAPH-004 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested |
| MVP-FR-007 | Jira graph queryable with provenance | FR-ONTO-001, FR-GRAPH-002 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested |
| MVP-FR-008 | Code graph with exact source locations | FR-CODE-001/004 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested |
| MVP-FR-009 | Meta graph | FR-GRAPH-005 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested |
| MVP-FR-010 | Cross-graph linking, demo path traversable both ways | FR-GRAPH-006 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested |
| MVP-FR-011 | Provenance: evidence + creation status + lineage endpoint | FR-PROV-001/002 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested |
| MVP-FR-012 | Graph validation with quarantine of hard-invalid data | FR-VALID-001/002 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested |
| MVP-FR-013 | Versioned query API with policy enforcement | FR-QUERY-001/006 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested |
| MVP-FR-014 | Impact analysis golden blast-radius set | FR-QUERY-003 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested |
| MVP-FR-015 | Path query golden ordered sequence | FR-QUERY-002 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested |
| MVP-FR-016 | Search/query UI on real APIs | FR-UI-001 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested |
| MVP-FR-017 | Graph visualizer bounded subgraphs | FR-UI-002 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested |
| MVP-FR-018 | Admin ingestion/validation UI with real counts | FR-ADMIN-001/002 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested |
| MVP-FR-019 | VS Code extension symbol context | FR-VSCODE-001/002 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested; installed-VSIX acceptance = external gate |
| MVP-FR-020 | Local GraphRAG with citations and model-down fallback | FR-RAG-001/002/003 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested |
| MVP-FR-021 | TraceImpactAgent with allowlisted tools and budgets | FR-AGENT-003 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested |
| MVP-FR-022 | MCP read-only core graph access, no write tools | FR-MCP-001/002 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested |
| MVP-FR-023 | Structured correlation-aware logging, no secrets | NFR-OPS-001 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested |
| MVP-FR-024 | Machine-readable metrics | NFR-OPS-002 | P1-MVP | MVP-requirements.md | Done (code-evidence policy; flipped from Partial in Pass 8) | tested |
| MVP-FR-025 | Checksummed backup artifact | NFR-REL-002 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested (logical backup); native backup = external gate |
| MVP-FR-026 | Restore reproduces counts and golden queries | NFR-REL-002 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested (restore receipts in historical audits) |
| MVP-FR-027 | Automated test suites and report | NFR-MAINT-001 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested (unit 1842 passed / 1 skipped / 0 failed; see Runtime Verification Receipts); remote CI observation = external gate |
| MVP-FR-028 | End-to-end clean-reset demo incl. backup/restore | FR-GRAPH-006, FR-AGENT-003 | P1-MVP | MVP-requirements.md | Done (code-evidence policy) | tested (demo rehearsals recorded); note demo-readiness audit still lists G2 P6-P10 and KGR phases 9/10 as partial under certification policy |

Truth notes on the MVP register: (1) `tickets/ticket-20261004-003.md` records that a conservative full-doc scan (156 files) extracted 761 IDs with 108 Partial / 653 Missing / 0 Done under a stricter conservative policy, before the code-evidence policy was adopted — the 28/28 Done above is a policy-dependent statement, not a universally agreed fact. (2) The "MVP evidence coverage 3/28 (10.71%)" figure quoted in several audits is an annotation-coverage metric of the evidence-linking tooling, explicitly "not an application-completion percentage" per its own receipt.

## Normative Document Contradictions And Resolutions

Added 2026-10-07 from the independent reader digests (READER A files 00-19, READER B files 20-39, READER G docs/tickets). Each entry states the conflict, the evidence, and the resolution this document adopts.

1. **Graph backend: "HugeGraph only" vs multi-backend.** Files `07-component-architecture.md` and `08-deployment-architecture.md` (and the MVP-implementation-plan's decision list) state Architecture Decision #2 as "HugeGraph is the only mandatory database"; connector docs 20/26 read as HugeGraph-exclusive. File `06-architecture.md` (Updated 2026-10-06, "Pass 5") states "HugeGraph is the default mandatory database; additional backends are pluggable" (Neptune openCypher, in-process Memory; `config/graph-store.yaml`, `EOIP_GRAPH_BACKEND`), and `76-multi-backend.md` documents the implemented `create_graph_store()` registry over HugeGraph/Neptune/Neo4j/Memory. **Resolution adopted: multi-backend wins** — 06 is the newer document and describes implemented, spot-verified code (`graph/backends.py`, `neptune.py`, `neo4j.py` all confirmed present by AUDIT-CODE); 07/08 are stale copies. Residual tension: the optional Neptune backend implies an external AWS endpoint, which no reconciled document squares with NFR-SEC-001's no-egress rule; Neptune must be treated as an explicitly configured exception.
2. **Schema drift between 06 (as-built) and 11 (normative MVP schema).** File 11's normative 20 edge labels lack `TRACES_TO`, `EVIDENCE_FOR`, `COMMITTED_TO`, `MERGED_VIA`, `DEPLOYED_BY`, which 06 lists as core; 06's vertex list includes `Pipeline`, `Team`, `Organisation`, `Service`, `Endpoint`, `Container`, `Deployment`, `Finding` where 11 has `PipelineRun`, `Branch`, `Dependency`, `KnowledgeSpace`, `AgentRun`, `ValidationFinding`; 06 names 14 graph domains where FR-GRAPH-002's text gives an illustrative list. **Resolution adopted: the as-built 06 lists win** (06 is newer and import-verified: AUDIT-CODE counted 74 vertex labels and 68 edge labels live). File 11 remains the historical MVP baseline; the drift is additive expansion, not a behavioral conflict.
3. **Undeclared requirement IDs defined only in 06 / the assessed report.** `FR-GRAPH-011` (multi-backend GraphStore registry, P2) is referenced in 06's Applicable Requirements but is not defined in file 03, whose catalog stops at FR-GRAPH-010; the assessed-gap-report's Pass-5 additions list both `FR-GRAPH-011` (multi-backend registry) and `FR-GRAPH-012` (Neptune adapter), neither with a normative WHAT/WHY/HOW entry in file 03. Similarly, READER B found `FR-QUERY-009` (natural-language query processor) defined in `25-query-engine-requirements.md` but absent from file 03's 67-ID catalog. **Resolution: treat these as real requirements whose definitions live outside file 03; file 03 is not the complete FR universe it appears to be.**
4. **Verbatim boilerplate duplication across the 00-19 file set (and beyond).** The "Engineering rules" (5 bullets) and "Validation / definition of done" (5 bullets) blocks are verbatim-identical in files 01, 02, 05, 07-19 (16 files) and appear with title-case headings in 06; the 10 "Architecture decisions" are verbatim in 07 and 08 and near-identical in 06; the "Phase 1 security baseline" (9 bullets) and "MVP benchmark definition" paragraph are verbatim-duplicated between 00 and 04 (and again in 46/47 and MVP-requirements.md / MVP-implementation-plan.md); the vertical-slice scope paragraph is verbatim in 01, 02, 05; the Docker-host mermaid diagram is verbatim in 00, 06, 08. READER B measured roughly 60-70% shared template text across files 20-39, and found docs 31/33/34/38 carry little or no unique content. **Resolution: duplication is recorded, not harmonized — single-sourcing these blocks is a documentation-debt item, not a requirement conflict.**
5. **READER G F.3 factual contradictions between current (non-historical) docs:**
   - `docs/61-demo-playbook.md` section 10 says `docker.ps1 down` removes Docker volumes ("next up starts fresh") — **wrong** per `docs/docker-local.md` and `docs/hubble-local.md`, which both state `down` retains volumes. Resolution: docker-local/hubble-local win; the playbook line is a stale/incorrect statement.
   - `docs/ontology.md` line 249 claims that if HugeGraph is unavailable "the system falls back to MemoryGraphStore for local dev" — conflicts with `docker-local.md` ("the in-memory store is used by unit tests only"), `docs/file-parsing.md` ("MemoryGraphStore is only the test harness"), and the `graph/backends.py` registry model (backend selection is explicit configuration, not silent fallback). Resolution: the registry-model docs win; ontology.md line 249 is stale.
   - **MCP tool-name/count drift:** 15 tools (docker-local.md and older phase-completion sections) vs 17 (api-reference.md and the phase-completion final certification) vs 18 (actual `@mcp.tool()` count in `apps/mcp/main.py` per AUDIT-CODE) vs the demo playbook's older short names (`search`, `entity`, `path`, `impact`, ...). Worse, api-reference.md's 17 listed names do not match the implemented tool names at all. Resolution: code wins — 18 tools; all doc inventories are stale to different degrees.
   - **IngestionRun status vocabulary:** `docs/ingestion.md` uses PENDING/RUNNING/DONE/FAILED; acceptance and rehearsal documents use SUCCEEDED/PARTIAL/HELD. Unresolved vocabulary drift between feature doc and acceptance docs.
   - **DLQ/state path drift:** `docs/ingestion.md` writes `deploy/dlq/...` and `deploy/checkpoints/...`; docker-local/hubble-local/file-parsing describe the container `/data/...` volume layout. Same logical stores, divergent documented paths.
   - **ADR-001 naming drift:** `docs/adr-001-g2-contract-and-revision-model.md` says `GraphRevision` where `docs/ontology.md` and other docs say `EntityRevision` — same concept, two names.
   - **Test-count drift:** `tickets/requirements-map.md` claims "7 native tests" for the VS Code extension where `tickets/ticket-20261004-005.md` body says 4 native protocol/driver tests. Minor numeric drift between coordination artifacts.
6. **Encoding / mojibake note (READER G F.7):** `docs/audit-2026-10-06/assessed-gap-report.md` contains mojibake (`â€”` for em-dashes, `â†'`-style arrow corruption), indicating a UTF-8 encoding mishap during its generation; it and `hubble-local.md`, `g2-traceability.md`, `ticket-20261004-005.md`, and `requirements-map.md` carry CR line endings. Cosmetic, but any quotation from those files should be re-transcribed rather than copy-pasted.

## Honest Code-Evidence Verdict

Added 2026-10-07. This section condenses the independent AUDIT-CODE verification of `docs/audit-2026-10-06/assessed-gap-report.md` against the actual repository (about 85 evidence file/line references spot-checked, all quantitative claims re-counted, both coverage gates re-run, the full pytest suite executed, the frontend built, and git state inspected).

**Headline verdict:** the report is substantially accurate about *what code exists* — capability-level claims are approximately 90% trustworthy, and the test suite is genuinely green. But the per-ID Done counts (296 GAP, 364 G2, 802 total) are artifacts of a self-satisfied string-match coverage gate, not independent behavioral verification:

- The coverage gates in `packages/eoip/gaps/coverage.py` are literal ID-string matchers: a requirement is "done" iff its ID appears at least once in any source file and at least once in any test file — comments included, no semantic check.
- **113 of the 296 GAP IDs (38%) have as their sole implementation+test evidence two docstring comment blocks** — the ID list in `gaps/enterprise_completion.py` (lines 1-58) and its mirror in `tests/unit/test_enterprise_gap_completion.py` (lines 1-48); that test file contains only 4 test functions for 181 claimed requirement references. The module does contain roughly 15 real deterministic classes covering perhaps 10-15 requirement clusters, but the per-ID linkage is manufactured by comment name-dropping.
- The G2 set (364 IDs) is better but similar in shape: 728 implementation references come from one 350-line file, `gaps/g2_readiness.py`, whose docstring lists ID ranges (e.g. 30 IDs from one comment line). Mitigating: `g2_readiness_report()` genuinely import-checks modules, file-existence-checks targets, and route-checks API paths per area — so G2 "Done" means "an existence/import matrix passes", not per-requirement behavioral proof.
- The assessed report discloses this policy in its own section 0.2 and 14.11; its executive-summary framing ("100% complete ... all marked Done with implementation and automated-test evidence") is nonetheless inflated.

**Agent catalog naming errors (assessed report section 7):** these listed classes do not exist under those names (capabilities and runtime enforcement are real):

| Report name | Actual code |
| --- | --- |
| TraceAgent | `AgentTraceStore` |
| EvaluationAgent | `evaluate_agents()` function |
| MemoryAgent | `MemoryPolicy` / `FileMemoryStore` |
| CatalogAgent | `build_agent_registry()` |
| ProposalAgent | `ProposalStore` |
| OrchestratorAgent | `AgentOrchestrator` |
| CommunityDetectionAgent | `CommunityAnalysisAgent` |
| GovernedAgent | no such class; `agents/governed.py` contains 11 specialist agents |
| KnowledgeDebtAgent / ExpertiseAgent | modules under `packages/eoip/graph/`, no agent classes of those names |

Also: the report cites `agents/agent_router.py` and `agents/knowledge_debt.py`, but both live under `packages/eoip/graph/`, and its FR-AGENT-005 evidence ("governed.py — disabled until governance exists") mischaracterizes the module.

**Stale or wrong line references (~10-15% of spot-checks; capability exists nearby in each case):**

| Report citation | Reality |
| --- | --- |
| `apps/api/extended.py:1251` = GET /metrics | Actually `extended.py:1294`; line 1251 is `ops/upgrade-plan` |
| `contracts/tool.py:14-20` = READ_TOOLS frozenset | READ_TOOLS lives at `agents/runtime.py:42`; tool.py holds ToolContract fields |
| `packages/eoip/observability.py` (NFR-OPS-001, MVP-FR-023) | No such file — it is the `packages/eoip/observability/` package (metrics.py, otel.py) |
| `deploy/docker-compose.yml:24` = HugeGraph (MVP-FR-001) | `hugegraph-server:` is at about line 29 |
| `apps/api/app.py:254` (path query), `:368` (impact) | Actually `:321` and `:336` |
| `apps/web/src/App.jsx:240-241, 325` (search UI, admin UI) | Stale — those lines are generic hooks; Admin/Studio render at about 591/771 |
| `eoip-engg-doc-pkg/06-architecture.md`, `.../76-multi-backend.md` | Directory is `EOIP-engg-doc-pkg` (uppercase) — paths break on case-sensitive filesystems |
| "`NoCodeStudio`" component (6 citations) | No such component; the real suite is `apps/web/src/studio/` (Studio.jsx, SchemaCanvas, QueryConsole, MappingDesigner, PipelineOrchestrator) — capability real, name invented |

**Under-reported capabilities (implemented, not credited in the report):** the 11 specialist agents in `agents/governed.py` (DataQuality, OntologyReview, ConnectorDiagnosis, DocumentationFreshness, EvidenceVerification, ArchitectureConformance, QueryOptimization, GraphInvestigator, KnowledgeCurator, ChangeImpact, IncidentInvestigation); a 40+ agent-type taxonomy in `graph/agent_router.py`; whole packages absent from the report — `authz/`, `marketplace/` (registry/packager/installer), `truth/`, `intelligence/laya`, `catalog/`, `ci/`, `events/`, `search/`, `graphtest/`, `fileparse/`; about 20 KGR web components beyond those listed (GeoMap, TimelineScrubber, GraphDiff, Playbooks, QueryBuilder, PRDashboard, SurprisePanel, TableView, and others) plus the full studio and admin suites; and test suites omitted from section 11 (`tests/runtime_dlq/`, `tests/runtime_hubble/`, `tests/integration/`).

**Quantitative corrections (measured vs claimed):** 18 MCP tools, not 17; 10 VS Code commands in `package.json`, not 8; AgentType literal has 21 values, not 22; `ALGORITHM_REGISTRY` has 29 entries, not "30+" (35 algorithm implementations verified by name across modules); 74 vertex labels and 68 edge labels (report's "40+" is conservative); 246 unique API route paths (app.py 113 + main.py 71 + extended router 84) — the report gives no total; container-hardening tests are 9, not 8; graph-algorithm tests are 34, not 12; JUnit records 1963 tests / 0 failures / 24 skipped (approximately 1939 passed) vs the report's "1922 passed, 33 skipped" — suite green, exact numbers drifted.

**Per-section trust ratings for the assessed report:**

| Report section | Rating | Basis |
| --- | --- | --- |
| Exec Summary / "100% Done" | C — inflated | Green tests real; completeness rests on the ID-reference gate; methodology disclosed only later |
| section 0 History/Pass-5 findings | B+ | Files verified; minor case-broken paths |
| section 1 Core FR | B+ | Capabilities real; ~10% stale/wrong line refs; observability path and "22 types" errors |
| section 2 NFR | B+ | All verified; path imprecision only |
| section 3 Resolved items | A- | All spot-checks passed |
| section 4 Formats/Languages | A | 12 export formats, 6 query languages confirmed |
| section 5 Algorithms | A- | 35 verified; registry is 29, not "30+" |
| section 6 Semantic pipeline | B+ | File + 12 tests verified; stages not deep-checked |
| section 7 Agent catalog | D+ | ~8 of 20 rows name nonexistent classes or wrong paths; undercounts real agents |
| section 8 GAPS | C+ | 8.1-8.5 real (NoCodeStudio name wrong); 8.6's 296/296 is gate-engineered (113 docstring-only) |
| section 9 G2 | B- | Gate reproduces; evidence = existence matrix + ID-range comments, disclosed in section 0.2 |
| section 10 Multi-backend | A- | All four backends present and substantive |
| section 11 Test coverage | B+ | Suite green confirmed (1963 tests, 0 failures); file-count and skip-count figures stale; two suites omitted |
| section 12 MVP | B+ | All capabilities real; several stale line refs |
| section 13 Docs | A- | All files exist; MCP tool-name doc stale; case-bug paths |
| section 14 Limitations | A- | Genuinely honest; the one section that discloses the weak gate methodology |

Git state at audit time: clean (`git status --porcelain` empty, no stashes, HEAD `e994254`); no broken or uncommitted state. Historical hygiene note: 193 XML/JSON artifacts are committed under `test-results/`.

## Runtime Verification Receipts

Added 2026-10-07 from the independent AUDIT-RUNTIME pass (commands actually executed or read from recorded artifacts; nothing inferred). Overall verdict: **RUNTIME-HEALTHY** — all executed pytest suites pass (exit 0), the 6-container Docker stack is up and healthy with live readiness and metrics endpoints, and the most recent recorded Playwright run passed. The only red signal is ruff.

- **Unit tests** (`tests/unit`, run twice, both exit code 0): collected 1843 (`--collect-only`: "1843 tests collected in 4.98s"); **passed 1842, skipped 1, failed 0**. The 1 skip is `tests/unit/test_marketplace.py:150`, a conditional branch skip ("corruption landed in zip structure rather than member data"). Wall time about 455 s and 429 s. Caveat: pytest's final `-q` summary line was consistently swallowed by Git-Bash output capture (observed 3 times); counts were derived exactly from 1843 progress markers (exactly one `s`, zero `F`/`E`) plus exit code 0 and the collection count.
- **Security + performance + contract** (combined, exit 0): **"56 passed, 1 warning in 9.63s"** — security 27 + contract 17 + performance 12 = 56, consistent with separate per-suite runs.
- **Docker stack** (`docker ps`): 6 containers, all "Up (healthy)":

| Container | Status | Port |
| --- | --- | --- |
| eoip-eoip-api-1 | Up 17h (healthy) | 127.0.0.1:8000 |
| eoip-eoip-web-1 | Up 17h (healthy) | 127.0.0.1:8080 |
| eoip-eoip-worker-1 | Up 17h (healthy) | — |
| eoip-eoip-mcp-1 | Up 44h (healthy) | 127.0.0.1:8001 |
| eoip-hubble-1 | Up 47h (healthy) | 127.0.0.1:8088 |
| eoip-hugegraph-server-1 | Up 2d (healthy) | 8080/tcp (internal) |

- **Live endpoints:** `curl http://localhost:8000/health/ready` returned **HTTP 200** with body `{"status":"ready"}`; `curl http://localhost:8000/metrics` returned **HTTP 200** with live Prometheus metrics (notable counters: `/health/live` 6071x200, `/health/ready` 5933x200, `/api/v1/admin/jobs` 920x200, `/api/v1/admin/stats` 919x200 plus 1 historical 503 — a single past blip, not current).
- **Playwright (apps/web):** `apps/web/test-results/.last-run.json` (mtime 2026-10-06 22:38) records `{"status":"passed","failedTests":[]}` for the current suite (testDir `./tests`, 8 spec files, 19 tests). One spec was actually re-run against the live stack: `tests/hubble.spec.js` → **3 passed, 4 skipped in 19.5s, exit 0**; the 4 skips are intentional opt-in tests gated on `EOIP_RUNTIME_HUBBLE=1`. The root `test-results/.last-run.json` (mtime 2026-10-03) records a failure, but it is a **stale artifact** of an older root-level run (no root playwright config or package.json exists); it is not representative of the current suite.
- **Ruff:** `.venv/Scripts/python -m ruff check .` → **exit 1, "Found 165 errors"** (97 auto-fixable with `--fix`, plus 16 more with `--unsafe-fixes`). Breakdown by rule: I001 x47 (unsorted imports), F401 x22 (unused import), BLE001 x19 (blind except), SIM115 x17 (open without context handler), UP037 x17, RUF012 x5, TRY004 x4, F841 x4, UP017 x3, RUF022 x3, RUF059 x3, F541 x3, DTZ011 x2, FURB162 x2, SIM114 x2, S110 x2, C408 x2, and 1 each of B017, B008, UP035, SIM201, SIM202, PYI034, PIE810, PERF102. Mostly mechanical; about 59% auto-fixable.
- **Test-function counts per suite directory** (unit count below collected items because of parametrization):

| Directory | `def test_` functions | Files |
| --- | --- | --- |
| tests/unit | 1617 | 154 |
| tests/integration | 2 | 1 |
| tests/security | 27 | 4 |
| tests/performance | 12 | 2 |
| tests/contract | 17 | 3 |
| tests/e2e (pytest) | 35 | 5 |
| tests/runtime_dlq | 15 | 15 |
| tests/runtime_hubble | 7 | 6 |
| apps/web/tests (Playwright) | 19 tests | 8 spec files |

- **Environment-dependent items (by design, not defects):** the 1 unit skip (branch-dependent); the 4 hubble Playwright skips (`EOIP_RUNTIME_HUBBLE=1` opt-in); `tests/e2e`, `tests/runtime_dlq`, and `tests/runtime_hubble` require the live stack / opt-in fixtures and were counted but not executed.
- **Other notes:** one historical 503 for `/api/v1/admin/stats` in the `/metrics` history (current readiness is 200); pytest `-q` summary-line loss through Git-Bash redirection is a tooling quirk of this environment, not a test failure; raw logs preserved at `.tmp/pytest-unit.log` and `.tmp/pytest-spc.log`.

## Supersession Chain And Historical Audit Provenance

Added 2026-10-07 from READER G's cross-file synthesis (F.1). Status claims in any older document below must be read through this chain; per the files' own declarations:

1. `docs/deployment-verification.md` (2026-10-02) — labeled "HISTORICAL ONLY" by `docs/eoip-development-audit-2026-10-03.md` section 3; its counts (123 tests, 2 UI tests) are long superseded.
2. `docs/application-audit-2026-10-02.md` — historical, carrying a 2026-10-04 superseding-verification banner; extended by the gap audit.
3. `docs/gap-audit-2026-10-02.md` — its "Original status summary" is self-marked historical ("Do not use this original table as the current backlog"); the dated remediation-batch sections remain the provenance record for each fix; its conservative statuses are declared superseded by the 2026-10-06 report.
4. `docs/eoip-development-audit-2026-10-03.md` — point-in-time at rev f5a2402 plus later remediation updates; its section 9 sign-off ("NOT DEMO-READY / NOT 100% COMPLETE") was conditional at writing and partially superseded inline.
5. `docs/phase-completion-audit-2026-10-03.md` — batch log with final certification 2026-10-04; its G2-P6..P10 PARTIAL table conflicts with the 2026-10-06 report's all-Done (different evidence policies: end-to-end certification vs code-reference). Also contains one internally stale line: "Items 16/19 remain incomplete" was not revised after its own gap-19 canonical-boundary batch closed item 19.
6. `docs/demo-readiness-audit-2026-10-03.md` — mixed: a current "enterprise remediation progress" header plus a labeled-historical 2026-10-04 verification section.
7. `docs/hubble-runtime-validation.md` (2026-10-05) and `docs/validation-evidence-phase1.md` (2026-10-04) — current evidence records for their scopes; the former explicitly retains FAIL receipts alongside PASS and states coverage is 66/271 operations PARTIAL with verdict NEEDS_SIGNOFF.
8. `docs/audit-2026-10-04/*` — **removed from the worktree** per the 2026-10-06 addendum; still referenced (now dangling links) by `tickets/ticket-20261004-003.md` and `tickets/requirements-map.md`.
9. `docs/audit-2026-10-06/*` (generated 2026-10-05, updated 2026-10-07, "Pass 8 final") — **self-declared single current assessed audit source**, superseding all of the above for status purposes, with the explicit caveat that its statuses rest on the "local code/test-evidence audit policy" and that live semantic acceptance, production scale, and customer infrastructure certification remain separate release gates.

## Open External Gates (Union)

Added 2026-10-07 from READER G's F.6 union of open gates consistently named across the docs corpus, deduplicated. These remain open regardless of the code-evidence-policy Done statuses above; each is outside what local code and tests can certify:

1. Live multi-node HA / Kubernetes / graph-cluster certification (including the HugeGraph PD/Store sharding shape, which `docs/deployment-ha.md` itself calls "not validated in this repo").
2. Live tenant connector verification with real third-party credentials (Jira, Confluence, ServiceNow, GitHub, GitLab) — all currently fixture/MockTransport-covered only.
3. Confluence attachment bytes and historical body retrieval.
4. Inferred semantic matching acceptance.
5. Native HugeGraph/RocksDB backup and crash-atomic multi-store recovery (gap item 16 / G2-P10 partially; the logical-archive track is implemented).
6. Webhook receipt rebasing.
7. Memory / audit / trace-history recovery.
8. Production-scale, hardware-backed benchmark: NFR-PERF-001 full profile plus HTTP workload on isolated HugeGraph with committed revision and external telemetry (docs/benchmarking.md: "remains partially open").
9. Release SBOM / license / no-egress evidence package.
10. Installed-VSIX verification and visual/manual VS Code extension acceptance.
11. Remote CI observation, publication, and independent QA review (tickets 003/004 blocked on exactly this).
12. User-import scope decision (ticket 001; the referenced spec was found not to exist — a quarantined phantom-work proposal).
13. Docker-backed / live-stack verification for the demo ticket (005).
14. Linux-image verification of the fileparse native dependencies (docs/file-parsing.md flags this as pending; the 2026-10-06 report's external-gate list does not mention it — a potential silent gap in the Pass 8 closure claims).
15. Operational coverage beyond the 66 of 271 operations demonstrated in the live rehearsal.
16. MVP evidence-annotation coverage (3/28 = 10.71%) — recorded here for completeness; its own receipt states it is "not an application-completion percentage".

## Honest Residual Gaps And Risks

| Risk ID | Truthful finding | Required mitigation |
| --- | --- | --- |
| RG-01 | Audit JSON says all gap rows are done, but this document did not execute exhaustive end-to-end business scenarios for every connector/client environment. | Run connector-specific acceptance packs against real Jira/GitLab/GitHub/Confluence/ServiceNow/client graph systems before release. |
| RG-02 | The local Docker deployment is evidence of runnable packaging, not proof of HA, security certification, or production scale. | Perform production deployment rehearsal, threat-model review, backup/restore drill, and load/soak tests. |
| RG-03 | Markdown requirements are rich and overlapping; reconstruction should preserve source traceability and avoid deleting apparently duplicated requirements without owner review. | Use this consolidated file as a controlled baseline and resolve duplicates through ADRs. |
| RG-04 | Graph database portability is intentionally flexible; backend-specific behavior must be validated per selected client backend. | Keep the graph contract tests backend-neutral and add backend acceptance tests for Neptune/Neo4j/HugeGraph as clients choose them. |
