=======
History
=======

1.0.0 (2019-10-29)
==================

- Improved handling of switch from DST to winter time.

0.2.2 (2019-08-20)
==================

- Improved error message in multi-file simple format when
  nfields_to_ignore was 1 or more and a line did not have enough fields.

0.2.1 (2019-07-17)
==================

- Fixed a crash when a file was empty in multi-file simple format.
- Improved error messages in multi-file simple format when the
  timestamps were badly ordered in a file or overlapping between files.

0.2.0 (2019-07-16)
==================

- Added multi-file option to simple format.
- Added configuration parameters "encoding" and "ignore_lines".

0.1.3 (2019-06-07)
==================

- Upgraded htimeseries to 1.0.
- Made dependencies more robust.

0.1.2 (2019-05-27)
==================

- Made parsing dates more robust in simple format.
- Fixed extreme slowness when thousands of records had to be inserted.
- Fixed unhelpful error message when file was out of order.

0.1.1 (2019-04-18)
==================

- Fixed a bug that prevented using a log file.

0.1.0 (2019-04-18)
==================

- Initial release
