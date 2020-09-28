# -*- coding: utf-8 -*-
"""echelon_form.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qdMxfS2Kn_iqZV5XiExVr9M_dr2__X5h

The program helps find the echelon and reduced echelon of an input matrix. 

@AUTHOR: NGUYEN HOANG NAM ANH

##Helper functions

**Input Matrix**
"""

import numpy as np
import scipy.linalg as ln

def input_matrix():

    """Prompts users to enter matrix's shape and entries."""

    #prompt for shape
    num_row = int(input("Number of rows: " ))
    num_col = int(input("Number of columns: "))

    matrix = np.empty((num_row,num_col))

    print("\nSuccess creating matrix " + str(num_row) +" x "+ 
          str(num_col)+ "! Enter the entries for each row.\n"+
          "Separate the entries by SPACE\n")
    
    return enter_entries(matrix, num_row, num_col)

def enter_entries(matrix, num_row, num_col):

  """Prompts users to enter the entries of each row."""

  for row in range(1, num_row+1):
      entries = entries_prompt(row)

      # check whether each row has enough number of entries input
      # (based on the shape input)
      while not has_enough_entries(entries,num_col):
        print ("Number of entries exceeds or goes under limit")
        entries = entries_prompt(row)

      matrix[row-1] = np.array(entries)
  print ("\nMatrix:\n", matrix)
  return matrix

def entries_prompt(row):
  
  """Prompts for each row's entries."""

  entries = input("R" + str(row) + ": ")
  entries = list(map(float, entries.strip().split(" ")))
  return entries

def has_enough_entries(entries, num_col):
  
  """Checks whether the row has enough number 
  of entries input.
  """
  return len(entries) == num_col

"""**Locate first non-zero column**"""

def find_first_non_zero_col(matrix, row_start, row_stop, col_stop):

  """
  Returns index of the first non-zero column of 
  a submatrix. This submatrix has indices of: 
  * rows: from row_start to row_stop (exclusive)
  * columns: from 0 (default) to col_stop (exclusive).

  If no such column is found, returns -1. 
  """
  col = 0

  while col < col_stop and is_zero_col(matrix, col, row_start, row_stop):
      col +=1

  if col < col_stop:
    return col
  else:
    return -1

def is_zero_col(matrix, col, row_start, row_stop):

  """Returns  true iff this is an all-zero column."""

  is_zero_entry = True 

  while is_zero_entry and row_start < row_stop:
    if(matrix[row_start, col] != 0):
      is_zero_entry = False

    row_start +=1

  return is_zero_entry

"""**Locate row containing first non-zero entry in a column**"""

def find_first_non_zero_row(matrix, row_start, col):

  """ 
  Finds the first non-zero extry of a non-zero column. 
  Returns the row index of this entry.
  """
  
  while (matrix[row_start, col]) == 0:
    row_start +=1

  return row_start

"""**Swap row**"""

def swap_row(matrix, row_i, row_j):

  """Swaps 2 rows of matrix."""
  E = np.eye(matrix.shape[0])

  E[row_i,row_i] = 0
  E[row_i,row_j] = 1

  E[row_j,row_j] = 0
  E[row_j,row_i] = 1

  return E @ matrix

"""**Scalar_multiply**"""

def scalar_multiply(matrix, k_times, row_i):

  """Multiplies a row of a matrix with a scalar."""

  E = np.eye(matrix.shape[0])
  E[row_i,row_i] = k_times

  return E @ matrix

"""**Add_row**"""

def add_row(matrix, k_times, row_timed, row_modified):
  
  """Adds k times Row i (the row is timed) to Row j (the row is modified)."""
  
  E = np.eye(matrix.shape[0])
  E[row_modified, row_timed] = k_times

  return E @ matrix

"""**Replace every entry below a certain entry with 0**"""

def replace_by_zero(matrix, col, main_row, row_start, row_stop, step):

  """
  Replaces all entries below (or above, depending on 
  the step) a specific entry with 0s. 
  All entries are in one column.
  """

  for r in range(row_start, row_stop, step):
    
      k_times = -matrix[r,col] / matrix[main_row,col]

      matrix = add_row(matrix, k_times, row_timed=main_row, row_modified=r)

  return matrix

"""**Find Echelon form of matrix**"""

def find_echelon(matrix):

  """Returns the echelon form of the matrix. """

  for row in range (0, matrix.shape[0]):
    #find the first non-zero column. Call it A
    firstNZC = find_first_non_zero_col(matrix, row_start=row, 
                                  row_stop=matrix.shape[0], 
                                  col_stop=matrix.shape[1])
    if (firstNZC == -1):
        break

    # find the first non-zero row in col A
    firstNZR = find_first_non_zero_row(matrix, row_start=row, col=firstNZC)

    # interchange the rows so that the top entry in col A is non-zero
    matrix = swap_row(matrix, row_i=row, row_j=firstNZR)
    
    # multiply top row with 1/a to produce leading 1
    a = matrix[row, firstNZC]
    matrix = scalar_multiply(matrix, k_times=1/a, row_i=row)

    # replace all below entries of A with 0s
    matrix = replace_by_zero(matrix, col=firstNZC, main_row=row, 
                           row_start=row+1, row_stop= matrix.shape[0], 
                           step=1)
  
  print ("\n> Echelon form: \n", matrix)
  return matrix

"""**Find reduced echelon form of matrix**"""

def find_reduced_echelon(matrix):  

  """Returns the reduced echelon form of the matrix (which is already 
  in Echelon form). """

  for row in range(matrix.shape[0]-1, -1, -1):
    for col in range(0, matrix.shape[1]):

      if (matrix[row, col] == 1):
        matrix = replace_by_zero(matrix, col, main_row=row, 
                               row_start=row-1, row_stop=-1, 
                               step=-1)
  print ("\n> Reduced Echelon form: \n", matrix)   
  return matrix

"""##Main function"""

def transform_to_echelon():
  try: 
    matrix = input_matrix()
    print ("\nLoading...")
    print ("\n...Solved!")
    echelon = find_echelon(matrix)
    reduced_echelon = find_reduced_echelon(echelon)
    
  except ValueError:
    print ("Invalid input. Check the number of rows/ columns" +
           " or matrix entries again!")

transform_to_echelon()