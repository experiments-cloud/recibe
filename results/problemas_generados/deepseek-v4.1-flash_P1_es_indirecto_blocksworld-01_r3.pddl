(define (problem blocks-5)
  (:domain blocks)
  (:objects
    a b c d e - block
  )
  (:init
    (clear d)
    (handempty)
    (on d e)
    (on e c)
    (on c a)
    (on a b)
    (ontable b)
  )
  (:goal (and
    (on d c)
    (on c b)
    (on b e)
    (on e a)
  ))
)
