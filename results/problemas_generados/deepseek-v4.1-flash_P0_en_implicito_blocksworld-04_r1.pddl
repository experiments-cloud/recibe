(define (problem BLOCKS-problem)
  (:domain BLOCKS)
  (:objects
    a b c d - block
  )
  (:init
    (ontable a)
    (ontable b)
    (ontable c)
    (ontable d)
    (clear a)
    (clear b)
    (clear c)
    (clear d)
    (handempty)
  )
  (:goal
    (and
      (on d c)
      (on c b)
      (on b a)
    )
  )
)
