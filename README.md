`epfl_idevelop.filter_eyaml`
============================

This role provides the `eyaml` filter, which lets store secrets in
encrypted form in your Ansible playbooks and roles.

Requirements
------------

A working `eyaml` command must be in the `PATH` — Try
<pre>
gem install hiera-eyaml
</pre>

Why Not Ansible Vault?
----------------------

- EYAML supports public-key encryption, which lets an operator add a
  secret without the authority to know the others
- Straightforward support for multiple encryption keys (e.g.
  development vs. production environment)
- Line-by-line encryption — Makes `git diff` work


Example Playbook and Variable Declaration
-----------------------------------------

In a task file (say, `roles/myrole/tasks/main.yml`):
```yaml
- Name: ssh private key
  copy:
      dest: /etc/ssh/ecdsa_key
      content: {{ privkey | eyaml(eyaml_keys) }}
```

In the vars file (e.g. `roles/myrole/vars/main.yml`):

```yaml
privkey: |
      ENC[PKCS7,MIICWW91IGNvdWxkIHRyeSBhbmQgYmFzZTY0LWRlY29kZSB0aGlzIGluIGEgYmlkIHRvIGNyYWNrIGEgcHJpdmF0ZSBrZXkgb2Ygb3VycywgYnV0IHlvdSdyZSBnb25uYSBiZSBkaXNhcHBvaW50ZWQuCg==]
eyaml_keys:
  priv: "/keybase/team/epfl_wp_test/eyaml-privkey.pem"
  pub: "{{ playbook_dir }}/../keys/eyaml-epfl_wp_test.pem"

```

To edit your vars file:

```eyaml edit -d \
  --pkcs7-public-key keys/eyaml-epfl_wp_test.pem \
  roles/myrole/vars/main.yml
```

Follow the instructions in the comments to create or change a secret.

References
----------

[EYAML]: https://puppet.com/blog/encrypt-your-data-using-hiera-eyaml
[Keybase]: https://keybase.io/


License
-------

This work may be freely distributed and re-used under the terms of
[the MIT License v2.0](https://www.apache.org/licenses/LICENSE-2.0)

Author Information
------------------

Please contact EPFL IDEV-FSD <idev-fsd@groupes.epfl.ch>.
