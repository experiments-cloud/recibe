(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a b c d e - block
  )
  (:init
    (ontable b)
    (on a b)
    (on c a)
    (on e c)
    (on d e)
    (clear d)
    (handempty)
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
