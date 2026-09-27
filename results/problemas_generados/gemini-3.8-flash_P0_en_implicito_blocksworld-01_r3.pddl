(define (problem BLOCKS-5-0)
  (:domain BLOCKS)
  (:objects
    a b c d e - block
  )
  (:init
    (handempty)
    (ontable b)
    (on a b)
    (on c a)
    (on e c)
    (on d e)
    (clear d)
  )
  (:goal
    (and
      (on d c)
      (on c b)
      (on b e)
      (on e a)
    )
  )
)
