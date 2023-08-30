## Test table (manual)

Pos.      Description                    Unit price   Qty          Total
--------- ---------------------- ------------------ -------- -----------
1         Engineering                          5000    1            5000
2         Commissioning                        6000    1            6000
          **Total**                                            **11000**
------------------------------------------------------------------------

 \
 \

## All Test Tables (\LaTeX)

Tables obtained by including here:

```\input{|"python ../xls2latex.py -f prices.xlsx"}```

\input{|"python ../xls2latex.py -f prices.xlsx"}

That seems to work, can we also refer to this table (with caption)? Refer to [@tbl:quotation-price].

The second table ([@tbl:table-2]) shows more data.

But: apparently the number format from the `Excel` tables is not honored if the values are formula results... Need to dig in to that.

**UPDATE**: Fixed in python script. Now the number format in the `xls` is honored. (Only tested with LibreOffice generated files!)

 \
 \

## Specific (\LaTeX)

A more refined usage like so:

```\input{|"python ../xls2latex.py -f prices.xlsx -s 'Quotation Price' --label=tbl:qp2"}```

\input{|"python ../xls2latex.py -f prices.xlsx -s 'Quotation Price' --label=tbl:qp2"}

Refer to [@tbl:qp2], which we already have once, maybe trouble, or not, if we specify the label!

So now we still need to solve the redirect of `stderr`, which is necessary for unknown reasons: bombs out with a `Broken Pipe Error`, only when calling the `python` script...

Ok, fixed, just redirect `stderr` to `/dev/null` within the `python` script.
