(define (problem BLOCKS-PROBLEM)
  (:domain BLOCKS)
  (:objects
    a b c d - block
  )
  (:init
    (ontable a)
    (ontable b)
    (ontable d)
    (on c b)
    (clear a)
    (clear c)
    (clear d)
    (handempty)
  )
  (:goal
    (and
      (on a b)
      (on b c)
      (on c d)
    )
  )
)
