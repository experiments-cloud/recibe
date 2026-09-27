(define (problem BLOCKS-PROBLEM)
  (:domain BLOCKS)
  (:objects
    a b c d - block
  )
  (:init
    (ontable a)
    (ontable d)
    (ontable b)
    (on b c)
    (clear a)
    (clear d)
    (clear c)
    (handempty)
  )
  (:goal (and
    (on a b)
    (on b c)
    (on c d)
  ))
)
