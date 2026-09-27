(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a b c d e - block
  )
  (:init
    (on d e)
    (on e c)
    (on c a)
    (on a b)
    (ontable b)
    (clear d)
    (handempty)
  )
  (:goal (and
    (on d c)
    (on c b)
    (on b e)
    (on e a)
  ))
)
